class Table:
    comment: str
    xx_table_name: str
    XX_TABLE_NAME: str
    XxTableName: str
    xxTableName: str
    xxtablename: str
    XXTABLENAME: str
    table_name: str
    TABLE_NAME: str
    tablename: str
    TABLENAME: str
    tableName: str
    TableName: str
    pk: dict = None
    columns: []


class Column:
    db_dataType: str
    comment: str
    column_name: str
    Column_Name: str
    COLUMN_NAME: str
    ColumnName: str
    columnname: str
    COLUMNNAME: str
    dataType: str
    data_length: int
    is_pk: bool


class Gcode:
    template_title: str
    template_base_name: str  # 文件名
    template_absolute_path: str  # 文件全路径
    template_content: str
    target_base_name: str
    target_absolute_path: str
    target_content: str
