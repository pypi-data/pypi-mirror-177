from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


class RACTSnowflakeHook(SnowflakeHook):
    ''' Custom SnowflakeHook for RACT with added functionalities, as for example to
    insert a CSV into a table.
    '''

    def __init__(self, *args, **kwargs) -> None:
        super(RACTSnowflakeHook, self).__init__(*args, **kwargs)


    def insert_csv(self, csv_path, csv_file_name, stage_name, schema_name,
                   table_name, recreate_table=False) -> None:
        ''' Inserts a local CSV file into a table
        '''
        put_command = 'PUT file://{} @{} OVERWRITE = TRUE'.format(
                csv_path + csv_file_name,
                stage_name
            )
        execution_info = self.run(put_command)

        # TODO - remove all `recreate_table` in the project
        # if recreate_table:
            # self.run('TRUNCATE TABLE IF EXISTS {}.{}'.format(
            #     schema_name, table_name))

        copy_into_command = '''
            COPY INTO {}.{}
            FROM @{}/
            FILES = ('{}.gz')
            FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY='"')
            -- ON_ERROR = SKIP_FILE_10
            ;'''.format(
                schema_name,
                table_name,
                stage_name,
                csv_file_name
            )
        print(copy_into_command)
        execution_info = self.run(copy_into_command)
