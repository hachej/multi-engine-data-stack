import typing as t
from datetime import datetime

from sqlmesh import ExecutionContext, model
from pyiceberg.catalog import load_catalog
import os 


@model(
    "reviews.staging_reviews",
    kind="FULL",
    cron="*/5 * * * *",
    columns={
        "reviewid": "string",
        "username": "string",
        "review": "string",
        "ingestion_timestamp": "timestamp",
        "source_s3_key":"string"
    },
    start='2024-07-01',
    enabled=os.environ.get("DUCKDB_ENABLED")
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: t.Any,
) -> None:
    print(start, end)

    # Setup catalog
    catalog = load_catalog("glue", **{"type": "glue",
                                    "s3.region":"eu-central-1",
                                    "s3.access-key-id": os.environ.get("AWS_ACCESS_KEY_ID"),
                                    "s3.secret-access-key":  os.environ.get("AWS_SECRET_ACCESS_KEY")
                            })

    # Load landing data in duckdb
    con = catalog.load_table("multiengine.landing_reviews").scan().to_duckdb(table_name="landing_reviews")

    # Compute model
    output = con.execute("""
        SELECT 
            reviewid,
            username,
            review,
            epoch_ms(ingestion_date) as ingestion_timestamp,
            source_s3_key              
        FROM landing_reviews
        QUALIFY
            row_number() OVER (PARTITION BY username, review order by ingestion_timestamp) =1;
    """).arrow()
    
    # Create Iceberg if not exists
    tables = catalog.list_tables("multiengine")
    if ("multiengine", "staging_reviews") not in tables:
        catalog.create_table(
            "multiengine.staging_reviews",
            output.schema,
            location="s3://sumeo-parquet-data-lake/staging/reviews")
    
    # Overwrite target Iceberg table
    catalog.load_table("multiengine.staging_reviews").overwrite(output)

    return output.to_pandas()
