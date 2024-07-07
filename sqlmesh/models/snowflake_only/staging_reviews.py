import typing as t
from datetime import datetime

from sqlmesh import ExecutionContext, model
from pyiceberg.catalog import load_catalog

@model(
    "reviews.staging_reviews",
    kind="FULL",
    columns={
        "reviewid": "string",
        "username": "string",
        "review": "string",
        "ingestion_timestamp": "timestamp",
    },
    enabled=False #"@IF(@gateway='duckdb', False, True)"
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: t.Any,
) -> None:
    print(start, end)

    catalog = load_catalog("glue", **{"type": "glue",
                                    "region_name":"eu-central-1",
                                    "s3.region":"eu-central-1",
                            })

    # load landing data in duckdb
    con = catalog.load_table("multiengine.landing_reviews").scan().to_duckdb(table_name="landing_reviews")

    # compute ouput
    output = con.execute("""
    SELECT 
        reviewid,
        username,
        review,
        epoch_ms(ingestion_date) as ingestion_timestamp              
    FROM landing_reviews
    QUALIFY
        row_number() OVER (PARTITION BY username, review order by ingestion_timestamp) =1;
    """).arrow()
    
    # create Iceberg if not exists
    tables = catalog.list_tables("multiengine")
    if ("multiengine", "staging_reviews") not in tables:
        catalog.create_table(
            "multiengine.staging_reviews",
            output.schema,
            location="s3://sumeo-parquet-data-lake/staging/reviews")
    
    # overwrite target Iceberg table
    catalog.load_table("multiengine.staging_reviews").overwrite(output)

    return output.to_pandas()
