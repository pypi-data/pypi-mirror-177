import os.path
import shutil
import time

from db_hammer.util.date import date_to_str
from jinja2 import Template

from gencode.common import *
from gencode.common.db import *
from gencode.common.utils import *


def get_data(table_name=None):
    obj = get_table_info(table_name)
    if not obj:
        raise UserWarning(f"数据库表不存在表 【{table_name}】")
    table = Table()
    table.comment = obj["comment"]
    table.XX_TABLE_NAME = str(obj["table_name"]).upper()
    table.xx_table_name = str(obj["table_name"]).lower()
    table.XxTableName = get_XxTableName(obj["table_name"])
    table.xxTableName = get_xxTableName(obj["table_name"])
    table.xxtablename = table.xxTableName.lower()
    table.XXTABLENAME = table.xxTableName.upper()
    table.XX = get_table_package(obj["table_name"]).upper()
    table.xx = get_table_package(obj["table_name"]).lower()

    table.table_name = get_table_name(obj["table_name"])
    table.TABLE_NAME = str(table.table_name).upper()
    table.tableName = get_TableName(obj["table_name"]).lower()
    table.tableName = get_tableName(obj["table_name"])
    table.TableName = get_TableName(obj["table_name"])
    table.columns = []

    if table_name is not None and table_name.lower() == table.xx_table_name:
        cols = get_columns_by_table(table_name)
        for c in cols:
            column = Column()
            column.comment = c["comment"]
            column.db_dataType = c["data_type"]
            column.dataType = get_dataType(c["data_type"], c["data_length"])
            column.data_length = c["data_length"]
            column.column_name = str(c["column_name"]).lower()
            column.COLUMN_NAME = str(c["column_name"]).upper()
            column.ColumnName = get_ColumnName(c["column_name"])
            column.columnName = get_columnName(c["column_name"])
            column.columnname = get_columnName(c["column_name"]).lower()
            column.COLUMNNAME = get_columnName(c["column_name"]).upper()
            column.is_pk = bool(c["is_pk"])
            if column.is_pk and table.pk is None:
                table.pk = column.__dict__
            table.columns.append(column)

    d = {
        "table": table,
        "date": date_to_str(format_str="%Y-%m-%d"),
        "datetime": date_to_str(),
        "author": Config.myself.get("author", ""),
        "mail": Config.myself.get("mail", ""),
        "sign": Config.myself.get("sign", ""),
    }
    d.update(table.__dict__)
    return d


def load_template(template, data) -> Gcode:
    """加载模板"""
    try:
        gcode = Gcode()
        gcode.template_title = template
        path = os.path.join(Config.templates_dir, Config.templates[template])
        gcode.template_absolute_path = os.path.abspath(path)
        gcode.template_content = open(gcode.template_absolute_path, 'r', encoding=Config.encoding).read()
        gcode.template_base_name = os.path.basename(Config.templates[template])

        # 渲染代码内容
        gcode.target_content = Template(gcode.template_content, **Config.jinja2_config).render(data,
                                                                                               **Config.jinja_global())
        # 渲染全路径
        path = os.path.join(Config.target_dir, Config.target_mapping.get(template, "./"))
        gcode.target_absolute_path = Template(path, **Config.jinja2_config).render(data, **Config.jinja_global())
        # 文件名
        gcode.target_base_name = Template(os.path.basename(path), **Config.jinja2_config).render(data,
                                                                                                 **Config.jinja_global())
        return gcode
    except Exception as e:
        logging.error(f"模板错误：{template} {e}")


def gen_target(gcode: Gcode):
    """生成目录和文件"""
    backups = []
    dirname = os.path.dirname(gcode.target_absolute_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
        logging.info("[\033[32m新建目录\033[0m]" + " ----> " + dirname)

    # 进行备份
    if Config.backup and os.path.isfile(gcode.target_absolute_path) and os.path.exists(gcode.target_absolute_path):
        target_dir = dirname + "_backup_" + str(int(time.time() * 1000))
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, gcode.target_base_name)
        shutil.copyfile(gcode.target_absolute_path, target_path)
        backups.append(target_path)
    gen_type = "[\033[31m修改\033[0m]" if os.path.exists(gcode.target_absolute_path) else "[\033[32m新建\033[0m]"
    with open(gcode.target_absolute_path, mode="wb+") as f:
        f.write(gcode.target_content.encode(encoding=Config.encoding))
    logging.info(gen_type + " ----> " + os.path.abspath(gcode.target_absolute_path))

    if len(backups) > 0:
        for b in backups:
            logging.info("备份代码：" + b)
        # i = input("是否删除本次备份文件（Y/N）")
        # if i.upper() == "Y":
        #     for b in backups:
        #         os.remove(b)


def render(data, template):
    # 渲染
    if template:
        logging.info(f"指定了模板文件：{template}")
        g = load_template(template, data)
        if g is not None:
            gen_target(g)
        return

    for template in Config.templates:
        g = load_template(template, data)
        if g is not None:
            gen_target(g)


def to_make_template(path):
    with open(path, mode="r", encoding=Config.encoding) as f:
        content = f.read()
        replace = Config.make_template.get("replace", {})
        for rep_key in replace:
            content = content.replace(rep_key, replace[rep_key], -1)

    with open(path, mode="wb+") as f:
        f.write(content.encode(encoding=Config.encoding))
