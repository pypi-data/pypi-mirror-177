''' Operator to sync tables from source Oracle DB Server into destination
Snowflake.
'''

import csv
from datetime import datetime
import os

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
import logging

from airflow.providers.oracle.hooks.oracle import OracleHook
from hooks.custom_snowflake_hook import CustSnowflakeHook

'''
Useful documentation to modify this Operator:
oracle hook: https://github.com/apache/airflow/blob/main/airflow/providers/oracle/hooks/oracle.py
oracle operator: https://github.com/apache/airflow/blob/main/airflow/providers/oracle/operators/oracle.py
'''

class OracleToSnowflake(BaseOperator):
    ui_color = '#bed9ab'

    def __init__(self,
                 source_schema,
                 source_table,
                 destination_schema,
                 destination_table,
                 fill_table_statement,
                 warehouse='LANDING',
                 database='LANDING_DEV',
                 role='ACCOUNTADMIN',
                 schema='PUBLIC',
                 recreate_table=False,
                 oracle_conn_id='ORACLE',
                 snowflake_conn_id='SNOWFLAKE',
                 **kwargs):
        super().__init__(**kwargs)
        self.source_schema = source_schema
        self.source_table = source_table
        self.destination_schema = destination_schema
        self.destination_table = destination_table
        self.fill_table_statement = fill_table_statement
        self.recreate_table = recreate_table
        self.oracle_conn_id = oracle_conn_id
        self.snowflake_conn_id = snowflake_conn_id

        self.snowflake_hook = CustSnowflakeHook(
            snowflake_conn_id=snowflake_conn_id,
            warehouse=warehouse,
            database=database,
            role=role,
            schema=schema,
        )

        self.oracle_hook = OracleHook(
            oracle_conn_id = self.oracle_conn_id
        )

    @property
    def oracledb_client(self):
        return self.oracle_hook.get_conn()

    def execute(self, context):
        ''' Gets all the data from source Oracle Database Server, inserts it into a
        temporary CSV, and load the CSV into Snowflake.

        Note that the CSV will be dropped to avoid consuming too much disk
        space.
        '''

        try:
            csv_path = 'include/tmp/'
            os.chdir(os.path.expanduser("~/airflow"))
            csv_file_name = '{}_{}_{}'.format(
                self.destination_schema,
                self.destination_table,
                datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            )

            complete_csv_path = '{}{}'.format(csv_path, csv_file_name)

            # self.insert_into_csv('SELECT * from foo', '/tmp/foo')
            self.insert_into_csv(
                self.fill_table_statement,
                complete_csv_path
            )

            self.snowflake_hook.insert_csv(
                csv_path=csv_path,
                csv_file_name=csv_file_name,
                stage_name='%{}'.format(self.destination_table),
                table_name=self.destination_table,
                schema_name=self.destination_schema,
                recreate_table=self.recreate_table)

        except Exception as e:
            raise e

        finally:
            # Removes the temporary file once it is inserted in Snowflake
            if os.path.exists(complete_csv_path):
                os.remove(complete_csv_path)


    def insert_into_csv(self, sql, csv_path):
        ''' Inserts results of a SQL from OracleDB into a CSV
        '''
        cursor = self.oracledb_client.cursor()
        
        cursor.execute(sql)

        with open(csv_path, 'w') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(col[0] for col in cursor.description)
            for row in cursor:
                writer.writerow(row)


class OracleToSnowflakePlugin(AirflowPlugin):
    name = 'oracle_to_snowflake_operator_plugin'
    operators = [OracleToSnowflake]