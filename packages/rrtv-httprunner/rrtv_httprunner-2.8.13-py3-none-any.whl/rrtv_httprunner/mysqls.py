import threading
from typing import Union

import pymysql
from loguru import logger
from pymysql.cursors import DictCursor

from rrtv_httprunner import exceptions
from rrtv_httprunner.exceptions import DBSelectFailure


class MySQLHandler(object):
    """
    初始化数据库
    """

    # 也可以继承 Connection 这里没有选择继承
    def __init__(self, driver: Union[str, dict], **kwargs):
        if driver is None:
            raise exceptions.DBError("mysql datasource not configured")
        try:
            driver = driver if isinstance(driver, dict) else eval(driver)
        except Exception as ex:
            raise exceptions.DBError(
                f"unable to connect to mysql using this configuration <{driver}>, please check the configuration") from None
        try:
            self.connect = pymysql.connect(
                host=str(driver["host"]),  # 连接名
                port=int(driver["port"]),  # 端口
                user=driver["user"],  # 用户名
                password=driver["password"],  # 密码
                charset=driver["charset"],  # 不能写utf-8 在MySQL里面写utf-8会报错
                database=driver["database"],  # 数据库库名
                cursorclass=DictCursor,  # 数据转换成字典格式
                **kwargs
            )
            # 创建游标对象  **主要**
            self.cursor = self.connect.cursor()
        except TypeError as ex:
            logger.error(f"""MYSQL数据库连接失败:{driver}""")
            raise exceptions.DBConnectionError(f"""MYSQL数据库连接失败:{driver}""")

    def query_one(self, query, args=None, hard=False):
        """
        查询数据库一条数据
        :param query: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        :param hard: 是否为严苛模式 如果为True 数据为空时会抛出异常
        """
        self.cursor.execute(query, args)
        # 将更改提交到数据库
        self.connect.commit()
        res = self.cursor.fetchone()
        if res is None and hard:
            raise DBSelectFailure(f"{query, args} 查询为空") from None
        return res

    def delete(self, sql, args=None):
        """
        删除数据库一条数据
        :param sql: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        """
        self.cursor.execute(sql, args)
        self.connect.commit()
        self.connect.rollback()
        return self.cursor.fetchone()

    def query_all(self, query, args=None, hard=False):
        """
        查询数据库所有数据
        :param query: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        :param hard: 是否为严苛模式 如果为True 数据为空时会抛出异常
        """
        self.cursor.execute(query, args)
        # 将更改提交到数据库
        self.connect.commit()
        res = self.cursor.fetchall()
        if res is None and hard:
            raise DBSelectFailure(f"{query, args} 查询为空") from None
        return res

    def query(self, query, args=None, one=True, hard=False):
        """
        主体查询数据
        :param query: 执行MySQL语句
        :param args: 与查询语句一起传递的参数(给语句传参) 元组、列表和字典
        :param one: one是True 时候执行query_one, 否则执行query_all
        :param hard: 是否为严苛模式 如果为True 数据为空时会抛出异常
        """
        if one:
            return self.query_one(query, args, hard)
        return self.query_all(query, args, hard)

    def insert(self, query, args=None):
        self.cursor.execute(query, args)
        # 将更改提交到数据库
        self.cursor.fetchone()
        self.connect.commit()
        return self.cursor.lastrowid

    def close(self):
        """
        关闭
        :return:
        """
        # 关闭游标
        self.cursor.close()
        # 断开数据库连接
        self.connect.close()

    def __del__(self):
        try:
            self.close()
        except AttributeError:
            pass

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MySQLHandler, "_instance"):
            with MySQLHandler._instance_lock:
                if not hasattr(MySQLHandler, "_instance"):
                    MySQLHandler._instance = object.__new__(cls)
        return MySQLHandler._instance
