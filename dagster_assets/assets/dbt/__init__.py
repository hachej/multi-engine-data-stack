from typing import Any, Mapping
from dagster import MetadataValue
from dagster import AssetExecutionContext, AssetKey, file_relative_path
from dagster_dbt import (
    DagsterDbtTranslator,
    DbtCliResource,
    dbt_assets,
    get_asset_key_for_model,
    DbtManifestAssetSelection
)
from dagster import asset, Config

DBT_PROJECT_DIR = file_relative_path(__file__, "../../../dbt")

dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)
dbt_parse_invocation = dbt_resource.cli(["parse"]).wait()
dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")

@dbt_assets(
    manifest=dbt_manifest_path,
    select='tag:duckdb'
)
def dbt_project_assets_duck(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build", "--profile", "duck"], context=context).stream()

@dbt_assets(
    manifest=dbt_manifest_path,
    select='tag:supabase'
)
def dbt_project_assets_supabase(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build", "--profile", "supabase"], context=context).stream()

duck_models = DbtManifestAssetSelection(manifest=dbt_manifest_path, select="tag:duckdb")
supabase_models = DbtManifestAssetSelection(manifest=dbt_manifest_path, select="tag:supabase")