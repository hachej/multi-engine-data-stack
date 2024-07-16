import typing as t
from datetime import datetime
import pyarrow as pa
import pandas as pd
from snowflake.snowpark.dataframe import DataFrame
from snowflake.cortex import Sentiment, Complete
from snowflake.snowpark.functions import col, concat, lit, current_timestamp, parse_json
from sqlmesh.core.model.kind import ModelKindName
from sqlmesh import ExecutionContext, model
from pyiceberg.catalog import load_catalog
import os 

@model(
    "reviews.prediction",
    kind=dict(
        name=ModelKindName.INCREMENTAL_BY_TIME_RANGE,
        time_column="ingestion_timestamp"
    ),
    cron="*/5 * * * *",
    columns={
        "reviewid": "string",
        "sentiment": "float",
        "classification": "string",
        "ingestion_timestamp": "timestamp"
    },
    start='2024-07-01',
    depends_on=["reviews.staging_reviews"],
    enabled=os.environ.get("SNOWFLAKE_ENABLED")
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: t.Any,
) -> DataFrame:
    
    print(start, end)

    context.snowpark.sql("ALTER ICEBERG TABLE REVIEWS.STAGING_REVIEWS REFRESH")

    df = context.snowpark.table("MULTIENGINE_DB.REVIEWS.STAGING_REVIEWS")
    
    df = df.filter(f"(ingestion_timestamp >= '{start}') and (ingestion_timestamp <= '{end}')").select("reviewid", "review", "ingestion_timestamp")
    
    df = df.withColumn(
        "sentiment",
        Sentiment(col("review"))
    )

    df = df.withColumn(
        "classification",
        Complete(
            "llama3-8b",
            concat(
               lit("Extract author, book and character of the following <quote>"),
               col("review"),
               lit("""</quote>. Return only a json with the following format {author: <author>, 
                   book: <book>, character: <character>}. Return only JSON, no verbose text.""")
            )
        )
    )

    df = df.select(
        "reviewid", 
        "sentiment",
        "classification",
        "ingestion_timestamp" 
    )

    schema = pa.schema(
                [
                    pa.field("REVIEWID", pa.string(), nullable=False),
                    pa.field("SENTIMENT", pa.float64(), nullable=True),
                    pa.field("CLASSIFICATION", pa.string(), nullable=True),
                    pa.field("INGESTION_TIMESTAMP", pa.timestamp('us'), nullable=False)
                ]
            )

    catalog = load_catalog("glue", **{"type": "glue",
                                    "s3.region":"eu-central-1",
                                    "s3.access-key-id": os.environ.get("AWS_ACCESS_KEY_ID"),
                                    "s3.secret-access-key":  os.environ.get("AWS_SECRET_ACCESS_KEY")
                            })
    
    # create Iceberg if not exists
    tables = catalog.list_tables("multiengine")
    if ("multiengine", "predictions") not in tables:
        catalog.create_table(
            "multiengine.predictions",
            schema,
            location="s3://sumeo-parquet-data-lake/staging/predictions")

    # append partition to Iceberg table
    catalog.load_table("multiengine.predictions").append(pa.Table.from_pandas(df.to_pandas(), schema=schema))

    context.snowpark.sql("ALTER ICEBERG TABLE REVIEWS.PREDICTION REFRESH")

    return df
