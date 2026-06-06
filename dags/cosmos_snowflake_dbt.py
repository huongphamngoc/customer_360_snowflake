from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
import os
from pathlib import Path

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 4),
    "retries": 1,
}

# Global variables
SNOWFLAKE_CONN_ID = os.getenv('SNOWFLAKE_CONN_ID', 'snowflake_default')
DBT_PROJECT_NAME = os.getenv('DBT_PROJECT_NAME', 'dbt_FMCG')
DBT_PROJECT_PATH = (
    (Path(__file__).parent / 'dbt' / DBT_PROJECT_NAME).resolve().as_posix()
)
DBT_EXECUTABLE_PATH = f"{os.getenv('AIRFLOW_HOME')}/dbt_venv/bin/dbt"

# Cosmos configurations
_project_config = ProjectConfig(
    dbt_project_path=DBT_PROJECT_PATH,
)

_profile_config = ProfileConfig(
    profile_name='default',
    target_name='dev',
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id=SNOWFLAKE_CONN_ID
    ),
)

_execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)

ENTITIES = {
    'Categories': {
        'table_name': 'Categories', 
        's3_folder': 'categories/'
    },
    'Cities': {
        'table_name': 'Cities', 
        's3_folder': 'cities/'
    },
    'Countries': {
        'table_name': 'Countries', 
        's3_folder': 'countries/'
    },
    'Products': {
        'table_name': 'Products', 
        's3_folder': 'products/'
    },
    'Customers': {
        'table_name': 'Customers', 
        's3_folder': 'customers/'
    },
    'Employees': {
        'table_name': 'Employees', 
        's3_folder': 'employees/'
    },
    'Sales': {
        'table_name': 'Sales', 
        's3_folder': 'sales/'
    }
}

with DAG(
    dag_id='DbtDag_FMCG_snowflake',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['elt', 'snowflake', 'dbt'],
) as dag:

    # Initialize dbt_transform using DbtTaskGroup
    dbt_transform = DbtTaskGroup(
        group_id='dbt_transform',
        project_config=_project_config,
        profile_config=_profile_config,
        execution_config=_execution_config,
    )

    # Data loading loop
    for entity_key, config in ENTITIES.items():
        
        table = config['table_name']
        folder_path = config['s3_folder']
        
        load_task = SQLExecuteQueryOperator(
            task_id=f'load_{entity_key}_to_snowflake',
            conn_id='snowflake_default',
            sql=f"""
                COPY INTO RAW.FMCG.{table}
                FROM @RAW.FMCG.my_s3_stage_direct/{folder_path}
                FILE_FORMAT = (FORMAT_NAME = RAW.FMCG.csv_format_for_load)
                PATTERN = '.*\\.csv';
            """
        )
    
        # Place the dependency INSIDE the loop.
        # This ensures all 7 data loading tasks complete before running dbt
        load_task >> dbt_transform