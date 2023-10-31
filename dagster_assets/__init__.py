import os
from dagster import (
    Definitions,
    FilesystemIOManager,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)
from .assets.raw_data.duckpond import DuckPondIOManager, DuckDB
from .assets import raw_data
from .assets.dbt import (
    DBT_PROJECT_DIR,
    dbt_project_assets_duck,
    dbt_project_assets_snow,
    duck_models,
    snow_models,
    dbt_resource,
)

raw_data_assets = load_assets_from_package_module(
    raw_data,
    group_name="raw_data",
    key_prefix=["raw_data"],
)

raw_data_update_job = define_asset_job(
    "raw_data_update", 
    selection=raw_data_assets)

duck_job = define_asset_job(
    "duck_job", 
    selection=duck_models)

snow_job = define_asset_job(
    "snow_job", 
    selection=snow_models)

DUCKDB_LOCAL_CONFIG=f"""
set s3_region="us-east-1";
set s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
set s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
"""

resources = {
    # this io_manager allows us to load dbt models as pandas dataframes
    "io_manager":  DuckPondIOManager("newsletter-multiengine-stack", DuckDB(DUCKDB_LOCAL_CONFIG), prefix="data/"),
    # this resource is used to execute dbt cli commands
    "dbt": dbt_resource,
}

defs = Definitions(
    assets=[dbt_project_assets_duck, dbt_project_assets_snow, *raw_data_assets],
    resources=resources,
    schedules=[
        ScheduleDefinition(job=raw_data_update_job, cron_schedule="*/2 * * * *"),
    ]
)

