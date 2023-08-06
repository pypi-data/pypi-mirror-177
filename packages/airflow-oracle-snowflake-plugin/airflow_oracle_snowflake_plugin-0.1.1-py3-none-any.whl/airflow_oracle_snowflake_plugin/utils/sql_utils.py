

def get_create_statement(table_name: str, columns_definition: list) -> str:
    ''' Given a table_name and its columns definition, returns the create table
    statement for that table in Snowflake syntax.

    Each entry in column definition is formed by ('column_name', 'column_type')

    Example of column definition:
    [
        ('foo', 'int'),
        ('bar', 'varchar(255)'),
    ]
    '''

    # transforms the columns definition to SQL
    columns_aux = ['{} {}'.format(col_name, col_type) for col_name, col_type in columns_definition]
    columns_sql = ',\n    '.join(columns_aux)  # 4 spaces instead of tab for consistency and unit testing

    # Creates the CREATE TABLE statement
    sql_res = '''CREATE TABLE IF NOT EXISTS {} (
    {}
);'''.format(table_name, columns_sql)
    return sql_res


def get_select_statement(table_name: str, schema_name: str,
                         columns_definition: list,
                         sql_server_syntax=False) -> str:
    ''' Given a table_name and its columns definition, returns the select table
    statement for that table in SQL Server syntax.

    Each entry in column definition is formed by ('column_name', 'column_type')

    Example of column definition:
    [
        ('foo', 'int'),
        ('bar', 'varchar(255)'),
    ]
    '''
    # transforms the columns definition to SQL
    if sql_server_syntax:
        columns_aux = ['[{}]'.format(col_name) for col_name, col_type in columns_definition]
    else:
        columns_aux = [col_name for col_name, col_type in columns_definition]

    columns_sql = ',\n    '.join(columns_aux)  # 4 spaces instead of tab for consistency and unit testing

    # Creates the SELECT statement
    if sql_server_syntax:
        sql_res = '''SELECT
    {}
FROM [{}].[{}];'''.format(columns_sql, schema_name, table_name)
    else:
        sql_res = '''SELECT
    {}
FROM {}.{}'''.format(columns_sql, schema_name, table_name)
    return sql_res