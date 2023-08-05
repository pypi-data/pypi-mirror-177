import os
from db_hammer.mysql import MySQLConnection
from db_hammer.oracle import OracleConnection
from gencode.common.config import Config
from gencode.common.sqls import SQL


def DbConnect():
    if os.environ.get('ORACLE_HOME', None) is None:
        os.environ["ORACLE_HOME"] = "/Users/liuzhuo/var/instantclient_19_8"
    c = Config.db_conf.copy()
    del c["table"]
    del c["db_type"]
    del c["db_name"]
    if Config.db_conf["db_type"].upper() == "MYSQL":
        c["caps"] = "a"
        return MySQLConnection(**c)
    elif Config.db_conf["db_type"].upper() == "ORACLE":
        c["caps"] = "a"
        return OracleConnection(**c)
    else:
        raise Exception("数据库类型暂不支持，请联系作者")


def get_table_info(table_name):
    with DbConnect() as db:
        return db.select_dict(sql=SQL["TABLES"][Config.db_conf["db_type"].upper()], params={
            "db_name": Config.db_conf["db_name"],
            "table_name": table_name,
        })


# 取表备注
def get_table_comment(table_name: str):
    sql = """
        Select TABLE_COMMENT AS comment from INFORMATION_SCHEMA.TABLES 
        Where table_schema = '{}' and  table_name='{}'
        """.format(Config.db_conf["db_name"], table_name)

    with DbConnect() as db:
        obj = db.select_value(sql=sql)
        return obj.replace("主表", "").replace("从表", "").replace("明细表", "").replace("关联表", "")


def get_columns_by_table(table):
    with DbConnect() as db:
        ls = db.select_dict_list(sql=SQL["COLUMNS"][Config.db_conf["db_type"].upper()], params={
            "db_name": Config.db_conf["db_name"],
            "table_name": table
        })
        for l in ls:
            if l["comment"] == "" or l["comment"] is None:
                l["comment"] = l["column_name"]
            else:
                l["comment"] = l["comment"].replace("\n\t", " ").replace("\n", " ").replace("\r", " ")

        return ls
