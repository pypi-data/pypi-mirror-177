from typing import Dict, Text, Any, NoReturn, List

import demjson3 as demjson
import jmespath
import requests
from jmespath.exceptions import JMESPathError
from jsonschema import ValidationError
from loguru import logger

from rrtv_httprunner import exceptions
from rrtv_httprunner.exceptions import ValidationFailure, ParamsError, EvalError
from rrtv_httprunner.models import VariablesMapping, Validators, FunctionsMapping
from rrtv_httprunner.parser import parse_data, parse_string_value, get_mapping_function
from rrtv_httprunner.utils import is_json


def get_uniform_comparator(comparator: Text):
    """ convert comparator alias to uniform name
    """
    if comparator in ["eq", "equals", "equal"]:
        return "equal"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_or_equals"]:
        return "less_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_or_equals"]:
        return "greater_or_equals"
    elif comparator in ["ne", "not_equal"]:
        return "not_equal"
    elif comparator in ["str_eq", "string_equals"]:
        return "string_equals"
    elif comparator in ["len_eq", "length_equal"]:
        return "length_equal"
    elif comparator in [
        "len_gt",
        "length_greater_than",
    ]:
        return "length_greater_than"
    elif comparator in [
        "len_ge",
        "length_greater_or_equals",
    ]:
        return "length_greater_or_equals"
    elif comparator in ["len_lt", "length_less_than"]:
        return "length_less_than"
    elif comparator in [
        "len_le",
        "length_less_or_equals",
    ]:
        return "length_less_or_equals"
    else:
        return comparator


def uniform_validator(validator, variables_mapping: VariablesMapping = None,
                      functions_mapping: FunctionsMapping = None, ):
    """ unify validator

    Args:
        functions_mapping:
        variables_mapping:
        validator (dict): validator maybe in two formats:

            format1: this is kept for compatibility with the previous versions.
                {"check": "status_code", "comparator": "eq", "expect": 201}
                {"check": "$resp_body_success", "comparator": "eq", "expect": True}
            format2: recommended new version, {assert: [check_item, expected_value]}
                {'eq': ['status_code', 201]}
                {'eq': ['$resp_body_success', True]}

    Returns
        dict: validator info

            {
                "check": "status_code",
                "expect": 201,
                "assert": "equals"
            }

    """
    check_item = ""
    expect_value = ""
    message = ""
    comparator = ""
    if not isinstance(validator, dict):
        raise ParamsError(f"invalid validator: {validator}")

    if "check" in validator and "expect" in validator:
        # format1
        check_item = validator["check"]
        expect_value = validator["expect"]
        message = validator.get("message", "")
        comparator = validator.get("comparator", "eq")
    elif "t1" in validator and "t2" in validator:
        check_item = validator["t1"]
        expect_value = validator["t2"]
        message = validator.get("message", "")
        comparator = "diff"
        kwargs = validator.get("kwargs", "")
        return {
            "check": check_item,
            "expect": expect_value,
            "assert": comparator,
            "kwargs": kwargs,
            "message": message,
        }
    elif "schema" in validator:
        check = validator["schema"][0]
        expect = validator["schema"][1]
        message = validator["schema"][2]
        comparator = "schema"
        return {
            "check": check,
            "expect": expect,
            "assert": comparator,
            "message": message,
        }
    elif len(validator) == 1:
        # format2
        comparator = list(validator.keys())[0]
        compare_values = validator[comparator]

        if not isinstance(compare_values, list) or len(compare_values) not in [2, 3, 4, 5]:
            raise ParamsError(f"invalid validator: {validator}")
        if len(compare_values) == 2 or len(compare_values) == 3:
            check_item = compare_values[0]
            expect_value = compare_values[1]
        if len(compare_values) == 4 or len(compare_values) == 5:
            condition = parse_data(
                compare_values[0], variables_mapping, functions_mapping
            )
            check_item = compare_values[1]
            try:
                eval_val = eval(condition)
                if eval_val is True:
                    expect_value = compare_values[2]
                else:
                    if compare_values[3] is None:
                        return
                    expect_value = compare_values[3]
            except NameError:
                raise EvalError(f"invalid expression: {compare_values[0]}")

        if len(compare_values) != 3 and len(compare_values) != 5:
            message = ""
        elif len(compare_values) == 3:
            message = compare_values[2]
        elif len(compare_values) == 5:
            message = compare_values[4]

    else:
        raise ParamsError(f"invalid validator: {validator}")

    # uniform comparator, e.g. lt => less_than, eq => equals
    assert_method = get_uniform_comparator(comparator)

    return {
        "check": check_item,
        "expect": expect_value,
        "assert": assert_method,
        "message": message,
    }


def extend_validate(api_validate: List[Dict], case_validate: List[Dict]) -> List[Dict]:
    api_assert_new: Dict = {}
    case_assert_new: Dict = {}
    extend_assert: List[Dict] = []
    extend_assert_dict: Dict = {}
    if not case_validate and api_validate:
        return api_validate
    for index, item1 in enumerate(api_validate):
        for k1, v1 in item1.items():
            api_assert_new[f"{k1}-{v1[0]}"] = api_validate[index]
    for index, item1 in enumerate(case_validate):
        for k1, v1 in item1.items():
            case_assert_new[f"{k1}-{v1[0]}"] = case_validate[index]
    for case_assert_key, case_assert_value in case_assert_new.items():
        for api_assert_key, api_assert_value in api_assert_new.items():
            if (case_assert_key not in list(api_assert_new.keys())) and (case_assert_key not in extend_assert_dict):
                extend_assert.append(case_assert_value)
                extend_assert_dict[case_assert_key] = case_assert_value
            if case_assert_key == api_assert_key:
                extend_assert.append(case_assert_value)
                extend_assert_dict[case_assert_key] = case_assert_value
            if (api_assert_key not in case_assert_new) and (api_assert_key not in extend_assert_dict):
                extend_assert.append(api_assert_value)
                extend_assert_dict[api_assert_key] = api_assert_value
    return extend_assert


class ResponseObject(object):
    def __init__(self, resp_obj: requests.Response):
        """ initialize with a requests.Response object

        Args:
            resp_obj (instance): requests.Response instance

        """
        self.resp_obj = resp_obj
        self.validation_results: Dict = {}

    def __getattr__(self, key):
        if key in ["json", "content", "body"]:
            try:
                value = self.resp_obj.json()
            except ValueError:
                response_dict = {}
                for attr in dir(self.resp_obj):
                    if attr == "text":
                        response_dict[attr] = getattr(self.resp_obj, attr)
                response_body = {}
                if "text" in response_dict and response_dict["text"] != "":
                    if is_json(response_dict["text"]):
                        response_dict['text'] = demjson.decode(response_dict['text'])
                        for k, v in response_dict['text'].items():
                            response_body[k] = v
                        for k, v in response_body["data"].items():
                            if isinstance(k, int):
                                response_body["data"][str(k)] = response_body["data"].pop(k)
                    else:
                        response_body["data"] = response_dict['text']
                value = response_body
                # value = self.resp_obj.content
        elif key == "cookies":
            value = self.resp_obj.cookies.get_dict()
        else:
            try:
                value = getattr(self.resp_obj, key)
            except AttributeError:
                err_msg = "ResponseObject does not have attribute: {}".format(key)
                logger.error(err_msg)
                raise exceptions.ParamsError(err_msg)

        self.__dict__[key] = value
        return value

    def _search_jmespath(self, expr: Text) -> Any:
        resp_obj_meta = {
            "status_code": self.status_code,
            "headers": self.headers,
            "cookies": self.cookies,
            "body": self.body,
        }
        if expr is None:
            return None
        try:
            key_list = [key for key in resp_obj_meta.keys()]
            flag = any(k in expr for k in key_list if not isinstance(expr, int))
            check_value = jmespath.search(expr, resp_obj_meta) if flag is True else expr
        except JMESPathError as ex:
            check_value = parse_string_value(expr)
            # logger.error(
            #     f"failed to search with jmespath\n"
            #     f"expression: {expr}\n"
            #     f"data: {resp_obj_meta}\n"
            #     f"exception: {ex}"
            # )
            # raise

        return check_value

    def extract(self, extractors: Dict[Text, Text], variables_mapping: VariablesMapping = None,
                functions_mapping: FunctionsMapping = None) -> Dict[Text, Any]:
        if not extractors:
            return {}

        extract_mapping = {}
        for key, field in extractors.items():
            field_value = self._search_jmespath(parse_data(field, variables_mapping, functions_mapping))
            if field_value == field:  # if not jmespath syntax
                field_value = parse_data(field, variables_mapping, functions_mapping)
                variables_mapping[key] = field_value

            extract_mapping[key] = field_value
            variables_mapping.update(extract_mapping)

        logger.info(f"extract mapping: {extract_mapping}")
        return extract_mapping

    def validate(
            self,
            validators: Validators,
            variables_mapping: VariablesMapping = None,
            functions_mapping: FunctionsMapping = None,
    ) -> NoReturn:

        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}

        self.validation_results = {}
        if not validators:
            return

        validate_pass = True
        failures = []

        for v in validators:

            if "validate_extractor" not in self.validation_results:
                self.validation_results["validate_extractor"] = []

            u_validator = uniform_validator(v, variables_mapping, functions_mapping)

            # check item
            if u_validator is not None:
                check_item = u_validator["check"]
                if isinstance(check_item, str):
                    if "$" in check_item:
                        # check_item is variable or function
                        check_item = parse_data(
                            check_item, variables_mapping, functions_mapping
                        )
                        check_item = parse_string_value(check_item)

                if check_item and isinstance(check_item, Text):
                    check_value = self._search_jmespath(check_item)
                else:
                    # variable or function evaluation result is "" or not text
                    check_value = check_item

                # comparator
                assert_method = u_validator["assert"]
                assert_func = get_mapping_function(assert_method, functions_mapping)

                # expect item
                expect_item = u_validator["expect"]
                # parse expected value with config/teststep/extracted variables
                expect_value = parse_data(expect_item, variables_mapping, functions_mapping)

                # message
                message = u_validator["message"]
                # parse message with config/teststep/extracted variables
                message = parse_data(message, variables_mapping, functions_mapping)

                validate_msg = f"assert {check_item} {assert_method} {expect_value}({type(expect_value).__name__})"

                validator_dict = {
                    "comparator": assert_method,
                    "check": check_item,
                    "check_value": check_value,
                    "expect": expect_item,
                    "expect_value": expect_value,
                    "message": message,
                }

                try:
                    if assert_method == "diff":
                        assert_func(check_value, expect_value, u_validator["kwargs"])
                    else:
                        assert_func(check_value, expect_value, )
                    validate_msg += "\t==> pass"
                    logger.info(validate_msg)
                    validator_dict["check_result"] = "pass"
                except (AssertionError, ValidationError) as ex:
                    validate_pass = False
                    validator_dict["check_result"] = "fail"
                    validate_msg += "\t==> fail"
                    validate_msg += (
                        f"\n"
                        f"check_item: {check_item}\n"
                        f"check_value: {check_value}({type(check_value).__name__})\n"
                        f"assert_method: {assert_method}\n"
                        f"expect_value: {expect_value}({type(expect_value).__name__})"
                    )
                    message = str(ex)
                    if message:
                        validate_msg += f"\nmessage: {message}"

                    logger.error(validate_msg)
                    failures.append(validate_msg)

                self.validation_results["validate_extractor"].append(validator_dict)

            if not validate_pass:
                failures_string = "\n".join([failure for failure in failures])
                raise ValidationFailure(failures_string)
