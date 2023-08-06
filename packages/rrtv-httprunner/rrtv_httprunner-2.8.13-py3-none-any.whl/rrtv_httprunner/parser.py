import ast
import builtins
import os
import re
import time
from typing import Any, Set, Text, Callable, List, Dict, Optional, Match, AnyStr

from jinja2 import Undefined, is_undefined
from jinja2.nativetypes import NativeEnvironment
from loguru import logger
from sentry_sdk import capture_exception

from rrtv_httprunner import loader, utils, exceptions, globalvar
from rrtv_httprunner.models import VariablesMapping, FunctionsMapping, data_enum
from rrtv_httprunner.utils import execute_sql, execute_cmd, get_statement_type, execute_redis, execute_mongo, \
    legitimate_method_call, execute_es, remove_bracket_first

absolute_http_url_regexp = re.compile(r"^https?://", re.I)

# use $$ to escape $ notation
dolloar_regex_compile = re.compile(r"\$\$")
# variable notation, e.g. ${var} or $var
variable_regex_compile = re.compile(r"\$\{([\w'\"\[\]\|.]+)\}|\$(\w+)")
variable_regex_compile_new = re.compile(r"\$(\w+)")
# function notation, e.g. ${func1($var_1, $var_3)}
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\S\w\s=,]*)\)\}")
function_regex_compile2 = re.compile(r"\$\{(\w+)\(([\$\S\w\s=,]*?)\)\}")
# function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\}\)\[\]\'\,\(\{\w\;\!\:\*\.\-/\s\=\,]*)\)\}")

suffix_regex_compile1 = r'\[\'(.*?)\'\]'
suffix_regex_compile2 = r"\[(.*?)\]"
suffix_regex_compile = re.compile(r"(\[\'.*?\'\]|\[.*?\])")
suffix = []
suffix2 = []


def parse_string_value(str_value: Text) -> Any:
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def build_url(base_url: Text, path: Text):
    """ prepend url with base_url unless it's already an absolute URL """
    if absolute_http_url_regexp.match(path):
        return path
    elif base_url:
        return "{}/{}".format(base_url.rstrip("/"), path.lstrip("/"))
    else:
        raise exceptions.ParamsError("base url missed!")


def regex_findall_variables(raw_string: Text) -> List[Text]:
    """ extract all variable names from content, which is in format $variable

    Args:
        raw_string (str): string content

    Returns:
        list: variables list extracted from string content

    Examples:
        >>> regex_findall_variables("$variable")
        ["variable"]

        >>> regex_findall_variables("/blog/$postid")
        ["postid"]

        >>> regex_findall_variables("/$var1/$var2")
        ["var1", "var2"]

        >>> regex_findall_variables("abc")
        []

    """
    try:
        match_start_position = raw_string.index("$", 0)
    except ValueError:
        return []

    vars_list = []
    while match_start_position < len(raw_string):

        # Notice: notation priority
        # $$ > $var

        # search $$
        dollar_match = dolloar_regex_compile.match(raw_string, match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            continue

        # search variable like ${var} or $var
        var_match = variable_regex_compile.match(raw_string, match_start_position)
        if var_match:
            var_name = var_match.group(1) or var_match.group(2)
            vars_list.append(var_name)
            match_start_position = var_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = raw_string.index("$", curr_position + 1)
        except ValueError:
            # break while loop
            break

    return vars_list


def regex_findall_functions(content: Text) -> List[Text]:
    """ extract all functions from string content, which are in format ${fun()}

    Args:
        content (str): string content

    Returns:
        list: functions list extracted from string content

    Examples:
        >>> regex_findall_functions("${func(5)}")
        ["func(5)"]

        >>> regex_findall_functions("${func(a=1, b=2)}")
        ["func(a=1, b=2)"]

        >>> regex_findall_functions("/api/1000?_t=${get_timestamp()}")
        ["get_timestamp()"]

        >>> regex_findall_functions("/api/${add(1, 2)}")
        ["add(1, 2)"]

        >>> regex_findall_functions("/api/${add(1, 2)}?_t=${get_timestamp()}")
        ["add(1, 2)", "get_timestamp()"]

    """
    try:
        return function_regex_compile.findall(content)
    except TypeError as ex:
        capture_exception(ex)
        return []


def extract_variables(content: Any) -> Set:
    """ extract all variables in content recursively.
    """
    if isinstance(content, (list, set, tuple)):
        variables = set()
        for item in content:
            variables = variables | extract_variables(item)
        return variables

    elif isinstance(content, dict):
        variables = set()
        for key, value in content.items():
            variables = variables | extract_variables(value)
        return variables

    elif isinstance(content, str):
        return set(regex_findall_variables(content))

    return set()


def parse_function_params(params: Text, func_name: Text) -> Dict:
    """ parse function params to args and kwargs.

    Args:
        params (str): function param in string

    Returns:
        dict: function meta dict

            {
                "args": [],
                "kwargs": {}
            }

    Examples:
        >>> parse_function_params("")
        {'args': [], 'kwargs': {}}

        >>> parse_function_params("5")
        {'args': [5], 'kwargs': {}}

        >>> parse_function_params("1, 2")
        {'args': [1, 2], 'kwargs': {}}

        >>> parse_function_params("a=1, b=2")
        {'args': [], 'kwargs': {'a': 1, 'b': 2}}

        >>> parse_function_params("1, 2, a=3, b=4")
        {'args': [1, 2], 'kwargs': {'a':3, 'b':4}}

    """
    function_meta = {"args": [], "kwargs": {}}

    params_str = params.strip()
    if params_str == "":
        return function_meta
    args_list: List = []
    # todo bug kv形式传参时会报错
    if "${" in params_str and ")}" in params_str:
        args_list.append(params_str)
        args_list = params_str.split(",")
    else:
        func_match = function_regex_compile.match(params_str, 0)
        if func_match:
            params_str = func_match.group(2)
        args_list = params_str.split(",")
    for arg in args_list:
        arg = arg.strip()

        if "=" in arg and "sql" not in func_name and "redis" not in func_name and "mongo" not in func_name and "cmd" not in func_name:
            key, value = arg.split("=", 1)
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta


def get_mapping_variable(
        variable_name: Text, var_name_whole: Text, variables_mapping: VariablesMapping
) -> Any:
    """ get variable from variables_mapping.

    Args:
        variable_name (str): variable name
        variables_mapping (dict): variables mapping

    Returns:
        mapping variable value.

    Raises:
        exceptions.VariableNotFound: variable is not found.

    """
    # TODO: get variable from debugtalk module and environ
    try:
        return variables_mapping[variable_name]
    except KeyError:
        return var_name_whole
        # raise exceptions.VariableNotFound(
        #     f"{variable_name} not found in {variables_mapping}"
        # )


def get_mapping_variable_jinja2(raw_string: Text, variables_mapping: VariablesMapping) -> Any:
    """ get variable from variables_mapping.

    Args:
        raw_string (str): to be parsed content
        variables_mapping (dict): variables mapping

    Returns:
        mapping variable value.

    Raises:
        exceptions.VariableNotFound: variable is not found.

    """
    mark = "mark" + str(round(time.time() * 1000))

    def default(var):
        if isinstance(var, str):
            if var.isnumeric():
                var = var + mark
        if is_undefined(var):
            return None
        return var

    env = NativeEnvironment(variable_start_string="${", variable_end_string="}")
    env.filters["default"] = default
    match_start_position = raw_string.index("$", 0)
    var_match = variable_regex_compile.match(raw_string, match_start_position)
    if var_match:
        if not get_function_compile_match(raw_string):
            val_findall = variable_regex_compile.findall(raw_string)
            for val in val_findall:
                val = val[0]
                if isinstance(val, str):
                    if "|default" not in val:
                        raw_string = raw_string.replace("${" + val + "}", "${" + val + "|default}")

    template = env.from_string(raw_string)
    value = template.render(variables_mapping)
    if isinstance(value, Text):
        value = value.replace(mark, "")
    return value


def get_mapping_function(
        function_name: Text, functions_mapping: FunctionsMapping
) -> Callable:
    """ get function from functions_mapping,
        if not found, then try to check if builtin function.

    Args:
        function_name (str): function name
        functions_mapping (dict): functions mapping

    Returns:
        mapping function object.

    Raises:
        exceptions.FunctionNotFound: function is neither defined in debugtalk.py nor builtin.

    """
    if function_name in functions_mapping:
        return functions_mapping[function_name]

    elif function_name in ["parameterize", "P"]:
        return loader.load_csv_file

    elif function_name in ["environ", "ENV"]:
        return utils.get_os_environ

    elif function_name in ["multipart_encoder", "multipart_content_type"]:
        # extension for upload test
        from rrtv_httprunner.ext import uploader

        return getattr(uploader, function_name)

    try:
        # check if HttpRunner builtin functions
        built_in_functions = loader.load_builtin_functions()
        return built_in_functions[function_name]
    except KeyError:
        pass

    try:
        # check if Python builtin functions
        return getattr(builtins, function_name)
    except AttributeError:
        pass

    raise exceptions.FunctionNotFound(f"{function_name} is not found.")


def get_function_compile_match(raw_string: Text) -> Optional[Match[AnyStr]]:
    match_start_position = raw_string.index("$", 0)
    func_match1 = function_regex_compile.match(raw_string, match_start_position)
    if func_match1 is not None:
        if legitimate_method_call(func_match1.group(2)) is True:
            return function_regex_compile.match(raw_string, match_start_position)
        else:
            return function_regex_compile2.match(raw_string, match_start_position)
    return None


def get_variable_compile_match(raw_string: Text) -> Optional[Match[AnyStr]]:
    match_start_position = raw_string.index("$", 0)
    var_match = variable_regex_compile_new.match(raw_string, match_start_position)
    if var_match:
        return var_match
    return None


def parse_string(
        raw_string: Text,
        variables_mapping: VariablesMapping,
        functions_mapping: FunctionsMapping,
) -> Any:
    """ parse string content with variables and functions mapping.

    Args:
        raw_string: raw string content to be parsed.
        variables_mapping: variables mapping.
        functions_mapping: functions mapping.

    Returns:
        str: parsed string content.

    Examples:
        >>> raw_string = "abc${add_one($num)}def"
        >>> variables_mapping = {"num": 3}
        >>> functions_mapping = {"add_one": lambda x: x + 1}
        >>> parse_string(raw_string, variables_mapping, functions_mapping)
            "abc4def"

    """

    if raw_string == "":
        return ""
    try:
        # 兼容老代码 如果为方法引用或$a格式，走老逻辑代码
        if get_variable_compile_match(raw_string):
            return parse_string_old(raw_string, variables_mapping, functions_mapping)
        if not get_variable_compile_match(raw_string):
            return parse_string_new(raw_string, variables_mapping, functions_mapping)
        if get_function_compile_match(raw_string):
            return parse_string_old(raw_string, variables_mapping, functions_mapping)
        if not get_function_compile_match(raw_string):
            return parse_string_new(raw_string, variables_mapping, functions_mapping)
        # if not get_variable_compile_match() or not get_function_compile_match():
        #     return parse_string_new(raw_string, variables_mapping, functions_mapping)
        # else:
        #     return parse_string_old(raw_string, variables_mapping, functions_mapping)
    except ValueError:
        # 如果不包含$，说明不存在变量，则直接返回
        return raw_string


def parse_string_old(
        raw_string: Text,
        variables_mapping: VariablesMapping,
        functions_mapping: FunctionsMapping,
) -> Any:
    try:
        match_start_position = raw_string.index("$", 0)
        parsed_string = raw_string[0:match_start_position]
    except ValueError:
        parsed_string = raw_string
        return parsed_string

    while match_start_position < len(raw_string):

        # Notice: notation priority
        # $$ > ${func($a, $b)} > $var

        # search $$
        dollar_match = dolloar_regex_compile.match(raw_string, match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            parsed_string += "$"
            continue

        # search function like ${func($a, $b)}
        func_match1 = function_regex_compile.match(raw_string, match_start_position)
        if func_match1 is not None:
            if legitimate_method_call(func_match1.group(2)) is True:
                func_match = function_regex_compile.match(raw_string, match_start_position)
            else:
                func_match = function_regex_compile2.match(raw_string, match_start_position)
        else:
            func_match = None
        if func_match:
            func_name = func_match.group(1)
            func = get_mapping_function(func_name, functions_mapping)
            func_params_str = func_match.group(2)
            function_meta = parse_function_params(func_params_str, func_name)
            args = function_meta["args"]
            kwargs = function_meta["kwargs"]
            parsed_args = parse_data(args, variables_mapping, functions_mapping)
            parsed_kwargs = parse_data(kwargs, variables_mapping, functions_mapping)

            try:
                func_eval_value = func(*parsed_args, **parsed_kwargs)
            except Exception as ex:
                logger.error(
                    f"call function error:\n"
                    f"func_name: {func_name}\n"
                    f"args: {parsed_args}\n"
                    f"kwargs: {parsed_kwargs}\n"
                    f"{type(ex).__name__}: {ex}"
                )
                raise

            func_raw_str = "${" + func_name + f"({func_params_str})" + "}"
            if func_raw_str == raw_string:
                # raw_string is a function, e.g. "${add_one(3)}", return its eval value directly
                return func_eval_value

            # raw_string contains one or many functions, e.g. "abc${add_one(3)}def"
            parsed_string += str(func_eval_value)
            match_start_position = func_match.end()
            continue

        # search variable like $var
        var_match = variable_regex_compile.match(raw_string, match_start_position)
        if var_match:
            var_name = var_match.group(1) or var_match.group(2)
            var_name_whole = var_match.group(0)
            var_value = get_mapping_variable(var_name, var_name_whole, variables_mapping)
            global suffix
            global suffix2
            # suffix_var = suffix_regex_compile.findall(raw_string)
            # return eval(str(var_value)+"".join(parse_data(suffix_var, variables_mapping, functions_mapping)))
            suffix_re = re.findall(var_name + suffix_regex_compile1, raw_string)
            if not suffix_re:
                suffix_re = re.findall(var_name + suffix_regex_compile2, str(raw_string))
            if suffix_re:
                if suffix_re[-1] == "]":
                    suffix2 = suffix_re[0]
                else:
                    suffix = suffix_re[0]
                if var_value is None:
                    if suffix is not None or suffix2 is not None:
                        replace_value1 = var_name_whole + "['" + suffix_re[0] + "']"
                        replace_value2 = var_name_whole + "[\"" + suffix_re[0] + "\"]"
                        replace_after_value = raw_string.replace(replace_value1, "None").replace(replace_value2,
                                                                                                 "None").replace(
                            var_name_whole, "None")
                        return replace_after_value if replace_after_value != "None" else None
                    else:
                        return var_value
                if not isinstance(var_value, Text) and not isinstance(var_value, int):
                    var_value = var_value[parse_data(suffix, variables_mapping, functions_mapping)]
                full_string = remove_bracket_first(raw_string)
                raw_string = full_string

            if f"${var_name}" == raw_string or "${" + var_name + "}" == raw_string:
                # raw_string is a variable, $var or ${var}, return its value directly
                return var_value

            # raw_string contains one or many variables, e.g. "abc${var}def"
            parsed_string += str(var_value)
            match_start_position = var_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = raw_string.index("$", curr_position + 1)
            remain_string = raw_string[curr_position:match_start_position]
        except ValueError:
            remain_string = raw_string[curr_position:]
            # break while loop
            match_start_position = len(raw_string)

        parsed_string += str(remain_string)
    return parsed_string


def parse_string_new(
        raw_string: Text,
        variables_mapping: VariablesMapping,
        functions_mapping: FunctionsMapping,
) -> Any:
    try:
        value = get_mapping_variable_jinja2(raw_string, variables_mapping)
        if isinstance(value, Undefined):
            return None
        return value
    except Exception:
        try:
            match_start_position = raw_string.index("$", 0)
            parsed_string = raw_string[0:match_start_position]
        except ValueError:
            return raw_string

    while match_start_position < len(raw_string):

        # Notice: notation priority
        # $$ > ${func($a, $b)} > $var

        # search $$
        dollar_match = dolloar_regex_compile.match(raw_string, match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            parsed_string += "$"
            continue

        # search function like ${func(${a}, $b)}
        func_match1 = function_regex_compile.match(raw_string, match_start_position)
        if func_match1 is not None:
            if legitimate_method_call(func_match1.group(2)) is True:
                func_match = function_regex_compile.match(raw_string, match_start_position)
            else:
                func_match = function_regex_compile2.match(raw_string, match_start_position)
        else:
            func_match = None
        if func_match:
            func_name = func_match.group(1)
            func = get_mapping_function(func_name, functions_mapping)
            func_params_str = func_match.group(2)
            function_meta = parse_function_params(func_params_str, func_name)
            args = function_meta["args"]
            kwargs = function_meta["kwargs"]
            parsed_args = parse_data(args, variables_mapping, functions_mapping)
            parsed_kwargs = parse_data(kwargs, variables_mapping, functions_mapping)

            try:
                func_eval_value = func(*parsed_args, **parsed_kwargs)
            except Exception as ex:
                logger.error(
                    f"call function error:\n"
                    f"func_name: {func_name}\n"
                    f"args: {parsed_args}\n"
                    f"kwargs: {parsed_kwargs}\n"
                    f"{type(ex).__name__}: {ex}"
                )
                raise

            func_raw_str = "${" + func_name + f"({func_params_str})" + "}"
            if func_raw_str == raw_string:
                # raw_string is a function, e.g. "${add_one(3)}", return its eval value directly
                return func_eval_value

            # raw_string contains one or many functions, e.g. "abc${add_one(3)}def"
            parsed_string += str(func_eval_value)
            match_start_position = func_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = raw_string.index("$", curr_position + 1)
            remain_string = raw_string[curr_position:match_start_position]
        except ValueError:
            remain_string = raw_string[curr_position:]
            # break while loop
            match_start_position = len(raw_string)
        try:
            if raw_string == remain_string:
                return raw_string
            remain_string = parse_string(remain_string, variables_mapping, functions_mapping)
        except Exception:
            pass
        parsed_string += str(remain_string)

    return parsed_string


def parse_data(
        raw_data: Any,
        variables_mapping: VariablesMapping = None,
        functions_mapping: FunctionsMapping = None,
) -> Any:
    """ parse raw data with evaluated variables mapping.
        Notice: variables_mapping should not contain any variable or function.
    """
    if isinstance(raw_data, str):
        global suffix
        global suffix2
        # suffix = []
        # content in string format may contains variables and functions
        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}
        # only strip whitespaces and tabs, \n\r is left because they maybe used in changeset
        raw_data = raw_data.strip(" \t")
        var_value = parse_string(raw_data, variables_mapping, functions_mapping)

        if get_statement_type(var_value) == data_enum.MYSQL:
            if data_enum.DB_CONFIG_SYMBOL in var_value:  # 指定环境执行sql
                value = execute_sql(var_value.split(data_enum.DB_CONFIG_SYMBOL)[1],
                                    var_value.split(data_enum.DB_CONFIG_SYMBOL)[0])
            else:
                value = execute_sql(variables_mapping[data_enum.MYSQL], var_value)
            if value is None:  # 如果为None说明非select方法
                return None  # 直接返回原字符串
            elif suffix2 == [] or suffix2 == "":  # 没有suffix后缀
                return value
            else:
                try:
                    return value[suffix2[0]]
                except KeyError:
                    raise exceptions.SuffixError("suffix name error")
        elif get_statement_type(var_value) == data_enum.CMD:
            return execute_cmd(var_value)
        elif get_statement_type(var_value) == data_enum.REDIS:
            if data_enum.DB_CONFIG_SYMBOL in var_value:  # 指定环境执行redis
                return execute_redis(var_value.split(data_enum.DB_CONFIG_SYMBOL)[1],
                                     var_value.split(data_enum.DB_CONFIG_SYMBOL)[0])
            else:
                return execute_redis(variables_mapping[data_enum.REDIS], var_value)
        elif get_statement_type(var_value) == data_enum.MONGO:
            if data_enum.DB_CONFIG_SYMBOL in var_value:  # 指定环境执行mongo
                return execute_mongo(var_value.split(data_enum.DB_CONFIG_SYMBOL)[1],
                                     var_value.split(data_enum.DB_CONFIG_SYMBOL)[0])
            else:
                return execute_mongo(variables_mapping[data_enum.MONGO], var_value)
        elif get_statement_type(var_value) == data_enum.ES:
            if data_enum.DB_CONFIG_SYMBOL in var_value:  # 指定环境执行es
                return execute_es(var_value.split(data_enum.DB_CONFIG_SYMBOL)[1],
                                  var_value.split(data_enum.DB_CONFIG_SYMBOL)[0])
            else:
                return execute_es(variables_mapping[data_enum.ES], var_value)
        else:

            if isinstance(var_value, dict):
                if suffix2:
                    match_start_position = raw_data.index("]", 0)
                    parsed_string = raw_data[match_start_position + 1:]
                    if parsed_string != "" or parsed_string is not None:
                        p = parse_string(parsed_string, variables_mapping, functions_mapping)
                        if suffix2:
                            val = var_value[suffix2]
                            return parse_string_value(str(val) + str(p))
                        else:
                            return parse_string_value(str(var_value) + str(p))
                    else:
                        return var_value[suffix2] if suffix2 != [] else var_value
                else:
                    return var_value

            else:
                if suffix2:
                    raw_string = str(var_value).replace(' ', '')
                    if suffix2[0] in raw_string and ":" in raw_string:
                        match_start_position = raw_string.index(":", 0)
                        parsed_string = raw_string[match_start_position + 1]
                        match_content_start_position = raw_string.index("{", 0)
                        match_content_end_position = raw_string.index("}", 0)
                        parsed_content_string = raw_string[match_content_start_position:match_content_end_position + 1]
                        var_value = raw_string.replace(parsed_content_string, parsed_string)
                        return var_value
                return var_value

    elif isinstance(raw_data, (list, set, tuple)):
        return [
            parse_data(item, variables_mapping, functions_mapping) for item in raw_data
        ]

    elif isinstance(raw_data, dict):
        parsed_data = {}
        for key, value in raw_data.items():
            parsed_key = parse_data(key, variables_mapping, functions_mapping)
            parsed_value = parse_data(value, variables_mapping, functions_mapping)
            parsed_data[parsed_key] = parsed_value

        return parsed_data

    else:
        # other types, e.g. None, int, float, bool
        return raw_data


def parse_variables_mapping(
        variables_mapping: VariablesMapping, functions_mapping: FunctionsMapping = None
) -> VariablesMapping:
    parsed_variables: VariablesMapping = {}

    while len(parsed_variables) != len(variables_mapping):
        for var_name in variables_mapping:

            if var_name in parsed_variables:
                continue

            var_value = variables_mapping[var_name]
            variables = extract_variables(var_value)

            # check if reference variable itself
            if var_name in variables:
                # e.g               # variables_mapping = {"token": "abc$token"}
                # variables_mapping = {"key": ["$key", 2]}
                raise exceptions.VariableNotFound(var_name)

            # check if reference variable not in variables_mapping
            not_defined_variables = [
                v_name for v_name in variables if v_name not in variables_mapping
            ]
            # if not_defined_variables:
            #     # e.g. {"varA": "123$varB", "varB": "456$varC"}
            #     # e.g. {"varC": "${sum_two($a, $b)}"}
            #     raise exceptions.VariableNotFound(not_defined_variables)

            try:
                parsed_value = parse_data(
                    var_value, variables_mapping, functions_mapping
                )
                extract_mapping = {var_name: parsed_value}
                variables_mapping.update(extract_mapping)
                # parsed_value = parse_data(
                #     var_value, parsed_variables, functions_mapping
                # )
            except exceptions.VariableNotFound:
                continue

            parsed_variables[var_name] = parsed_value

    return parsed_variables


def parse_parameters(parameters: Dict, ) -> List[Dict]:
    """ parse parameters and generate cartesian product.

    Args:
        parameters (Dict) parameters: parameter name and value mapping
            parameter value may be in three types:
                (1) data list, e.g. ["iOS/10.1", "iOS/10.2", "iOS/10.3"]
                (2) call built-in parameterize function, "${parameterize(account.csv)}"
                (3) call custom function in debugtalk.py, "${gen_app_version()}"

    Returns:
        list: cartesian product list

    Examples:
        >>> parameters = {
            "user_agent": ["iOS/10.1", "iOS/10.2", "iOS/10.3"],
            "username-password": "${parameterize(account.csv)}",
            "app_version": "${gen_app_version()}",
        }
        >>> parse_parameters(parameters)

    """
    parsed_parameters_list: List[List[Dict]] = []
    if parameters is not None and parameters != {}:
        globalvar.set_value("parameters", parameters)
    # load project_meta functions
    project_meta = loader.load_project_meta(os.getcwd())
    functions_mapping = project_meta.functions

    for parameter_name, parameter_content in parameters.items():
        parameter_name_list = parameter_name.split("-")

        if isinstance(parameter_content, List):
            # (1) data list
            # e.g. {"app_version": ["2.8.5", "2.8.6"]}
            #       => [{"app_version": "2.8.5", "app_version": "2.8.6"}]
            # e.g. {"username-password": [["user1", "111111"], ["test2", "222222"]}
            #       => [{"username": "user1", "password": "111111"}, {"username": "user2", "password": "222222"}]
            parameter_content_list: List[Dict] = []
            for parameter_item in parameter_content:
                if not isinstance(parameter_item, (list, tuple)):
                    # "2.8.5" => ["2.8.5"]
                    parameter_item = [parameter_item]

                # ["app_version"], ["2.8.5"] => {"app_version": "2.8.5"}
                # ["username", "password"], ["user1", "111111"] => {"username": "user1", "password": "111111"}
                parameter_content_dict = dict(zip(parameter_name_list, parameter_item))
                parameter_content_list.append(parameter_content_dict)

        elif isinstance(parameter_content, Text):
            # (2) & (3)
            parsed_parameter_content: List = parse_data(
                parameter_content, {}, functions_mapping
            )
            if not isinstance(parsed_parameter_content, List):
                raise exceptions.ParamsError(
                    f"parameters content should be in List type, got {parsed_parameter_content} for {parameter_content}"
                )

            parameter_content_list: List[Dict] = []
            for parameter_item in parsed_parameter_content:
                if isinstance(parameter_item, Dict):
                    # get subset by parameter name
                    # {"app_version": "${gen_app_version()}"}
                    # gen_app_version() => [{'app_version': '2.8.5'}, {'app_version': '2.8.6'}]
                    # {"username-password": "${get_account()}"}
                    # get_account() => [
                    #       {"username": "user1", "password": "111111"},
                    #       {"username": "user2", "password": "222222"}
                    # ]
                    parameter_dict: Dict = {
                        key: parameter_item[key] for key in parameter_name_list
                    }
                elif isinstance(parameter_item, (List, tuple)):
                    if len(parameter_name_list) == len(parameter_item):
                        # {"username-password": "${get_account()}"}
                        # get_account() => [("user1", "111111"), ("user2", "222222")]
                        parameter_dict = dict(zip(parameter_name_list, parameter_item))
                    else:
                        raise exceptions.ParamsError(
                            f"parameter names length are not equal to value length.\n"
                            f"parameter names: {parameter_name_list}\n"
                            f"parameter values: {parameter_item}"
                        )
                elif len(parameter_name_list) == 1:
                    # {"user_agent": "${get_user_agent()}"}
                    # get_user_agent() => ["iOS/10.1", "iOS/10.2"]
                    # parameter_dict will get: {"user_agent": "iOS/10.1", "user_agent": "iOS/10.2"}
                    parameter_dict = {parameter_name_list[0]: parameter_item}
                else:
                    raise exceptions.ParamsError(
                        f"Invalid parameter names and values:\n"
                        f"parameter names: {parameter_name_list}\n"
                        f"parameter values: {parameter_item}"
                    )

                parameter_content_list.append(parameter_dict)

        else:
            raise exceptions.ParamsError(
                f"parameter content should be List or Text(variables or functions call), got {parameter_content}"
            )

        parsed_parameters_list.append(parameter_content_list)

    return utils.gen_cartesian_product(*parsed_parameters_list)
