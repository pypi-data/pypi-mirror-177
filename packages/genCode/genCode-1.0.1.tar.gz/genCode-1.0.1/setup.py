from setuptools import setup
from gencode.version import VER

with open("./README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='genCode',
    version=VER,
    description='生成代码',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['gencode', 'gencode.common'],
    package_data={'gencode': ['README.md', 'LICENSE']},
    install_requires=['db-hammer', 'PyMySQL', 'cx_Oracle', 'click', 'jinja2', 'PyYAML'],
    entry_points={
        'console_scripts': [
            'gencode = gencode.main:run'
        ]
    },
)
