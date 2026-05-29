from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles.snowflake import SnowflakeUserPasswordProfileMapping
import os
from pathlib import Path
from pendulum import datetime
# Global variables
SNOWFLAKE_CONN_ID = os.getenv('SNOWFLAKE_CONN_ID', 'snowflake_default')
DBT_PROJECT_NAME = os.getenv('DBT_PROJECT_NAME', 'customer_360_snowflake')
# Adjust this path to point to where you store your dbt project
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
_default_args = {
    "retries": 1,
}
# dag instantiation
example_DbtDag_snowflake = DbtDag(
# Mandatory dag parameters
dag_id='DbtDag_customer360_snowflake',
# Mandatory Cosmos parameters
project_config=_project_config,
profile_config=_profile_config,
# Add optional Cosmos parameters as needed, for example
execution_config=_execution_config,
# Add optional dag parameters, for example:
start_date=datetime(2026, 5, 28),
schedule='@daily',
default_args=_default_args,
)