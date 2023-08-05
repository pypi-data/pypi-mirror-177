import logging
import os

import yaml

config_path = None


class Config:
    db_conf = None
    data_type_mapping = {}
    encoding = "utf-8"
    jinja2_config = {}
    myself = {}
    templates = []
    target_dir = None
    templates_dir = None
    target_mapping = {}
    table = None
    backup = True
    make_template = {}

    @staticmethod
    def load(config=None, table=None, backup=True):
        global config_path
        config_path = config
        if not os.path.isfile(config_path):
            logging.error(f"找不到配置文件：{config_path}")
            raise Exception("请输入正确的配置文件")
        try:
            with open(config_path) as f:
                yml = yaml.safe_load(f.read())
            Config.target_dir = yml.get("target_dir", os.path.dirname(__file__))
            Config.make_template = yml.get("make_template", {})
            Config.db_conf = yml["db_conf"]
            Config.data_type_mapping = yml["data_type_mapping"]
            Config.target_mapping = yml["target_mapping"]
            Config.jinja2_config["variable_start_string"] = "{{"
            Config.jinja2_config["variable_end_string"] = "}}"
            jinja2 = yml.get("jinja2", {})
            if jinja2:
                Config.jinja2_config.update(jinja2)
            Config.myself = yml.get("myself", {})
            Config.templates_dir = yml.get("templates_dir", os.path.dirname(__file__))
            Config.templates = yml.get("templates", [])
            Config.table = Config.db_conf.get("table", None)
            if table:
                Config.table = table
            if backup is None:
                Config.backup = yml.get("backup", False)
            Config.backup = backup
            while Config.table is None or str(Config.table).strip() == '':
                i = input(f"请输入表名：")
                print("")
                if i.strip() != '':
                    Config.table = i.strip()
                    break
        except Exception as e:
            err_lineno = e.__traceback__.tb_lineno
            logging.error(f"配置文件格式错误:{err_lineno} {str(e)} ")

    @staticmethod
    def jinja_global():
        return {
            "ljust": str.ljust,
            "rjust": str.rjust
        }
