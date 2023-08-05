import logging
import sys
import click

sys.path.append("../")
from gencode.common.config import Config
from gencode.common.data import render, to_make_template
from gencode.common import *


@click.command(help=get_help_txt(), context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--config', required=True, help="指定配置文件")
@click.option('--make-template', default=None, help="处理模板")
@click.option('--template', default=None, help="指定模板文件，如果指定了会忽略配置的设定")
@click.option('--table', default=None, help='指定数据库表')
@click.option('--backup/--no-backup', default=True, help='是否备份')
@click.option('--debug', default=False, help='输出Debug日志')
def run(config, make_template, table, backup, template, debug):
    try:
        if debug:
            logging.basicConfig(level=logging.DEBUG, format='%(filename)s[line:%(lineno)d] %(message)s')
        else:
            logging.basicConfig(level=logging.INFO, format='%(message)s')

        Config.load(config, table, backup)
        if make_template:
            to_make_template(make_template)
            return

        data = get_data(table_name=Config.table)
        render(data=data, template=template)
    except UserWarning as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info(f"""Bye ~""")


if __name__ == '__main__':
    run()
