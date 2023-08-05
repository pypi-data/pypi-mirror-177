import logging
import os
import re
from db_hammer.util.file import get_dir_files

from gencode.common import Gcode
from gencode.common.config import Config


def get_XxTableName(xx_table_name):
    ts = str(xx_table_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t.capitalize()
        else:
            s += t.capitalize()
    return s


def get_xxTableName(xx_table_name):
    ts = str(xx_table_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t
        else:
            s += t.capitalize()
    return s


def get_table_name(xx_table_name):
    ind = str(xx_table_name).find("_")
    return str(xx_table_name[ind + 1:]).lower()


def get_table_package(xx_table_name):
    ind = str(xx_table_name).find("_")
    return str(xx_table_name[0:ind]).lower()


def get_tableName(xx_table_name):
    table_name = get_table_name(xx_table_name)
    ts = str(table_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t
        else:
            s += t.capitalize()
    return s


def get_TableName(xx_table_name):
    table_name = get_table_name(xx_table_name)
    ts = str(table_name).lower().split("_")
    s = ''
    for t in ts:
        s += t.capitalize()
    return s


def get_columnName(coulum_name):
    ts = str(coulum_name).lower().split("_")
    s = ''
    for t in ts:
        if s == '':
            s = t
        else:
            s += t.capitalize()
    return s


def get_ColumnName(coulum_name):
    ts = str(coulum_name).lower().split("_")
    s = ''
    for t in ts:
        s += t.capitalize()
    return s


def get_dataType(db_data_type, data_length):
    # Config.load()
    logging.debug(Config.data_type_mapping.keys(), "==>", db_data_type, data_length)
    for d_key in Config.data_type_mapping.keys():
        d_keys = d_key.split("|")
        if db_data_type in d_keys or f"{db_data_type}({data_length})" in d_keys:
            return Config.data_type_mapping[d_key]
    return db_data_type


def get_help_txt():
    from gencode.version import VER
    return f"""
    GenCode 代码生成
    版本:{VER}  
    文档: https://github.com/liuzhuogood/GenCode
"""

