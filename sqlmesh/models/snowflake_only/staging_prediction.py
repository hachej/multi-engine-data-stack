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

@model(
    "reviews.prediction",
    kind=dict(
        name=ModelKindName.INCREMENTAL_BY_TIME_RANGE,
        time_column="ingestion_timestamp"
    ),
    # cron="@hourly",
    columns={
        "reviewid": "string",
        "sentiment": "float",
        "classification": "variant",
        "ingestion_timestamp": "timestamp",
        # "prediction_timestamp": "timestamp"
    },
    enabled= False, # TODO: fix this
    depends_on=["reviews.staging_reviews"]
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: t.Any,
) -> DataFrame:
    
    print(start, end)

    df = context.snowpark.table("REVIEWS.STAGING_REVIEWS").limit(2)
    
    df = df.filter(f"(ingestion_timestamp >= '{start}') and (ingestion_timestamp <= '{end}')").select("reviewid", "review", "ingestion_timestamp")
    
    df = df.withColumn(
        "sentiment",
        Sentiment(col("review"))
    )

    df = df.withColumn(
        "classification",
        parse_json(Complete(
            "llama3-8b",
            concat(
               lit("Extract author, book and character of the following <quote>"),
               col("review"),
               lit("</quote>. Return only a json with the following format {author: <author>, book: <book>, character: <character>}. Return only JSON, no verbose text.")
            )
        ))
    )
    # df = df.withColumn("prediction_timestamp", current_timestamp())

    df = df.select(
        "reviewid", 
        "sentiment",
        "classification", 
        "ingestion_timestamp",
        # "prediction_timestamp"
    )

    output= pa.Table.from_pandas(df.to_pandas()) 
    
    catalog = load_catalog("glue", **{"type": "glue",
                                "region_name":"eu-central-1",
                                "s3.region":"eu-central-1",
                        })
    
    # create Iceberg if not exists
    tables = catalog.list_tables("multiengine")
    if ("multiengine", "predictions") not in tables:
        catalog.create_table(
            "multiengine.predictions",
            output.schema,
            location="s3://sumeo-parquet-data-lake/staging/predictions")

    # append partition to Iceberg table
    catalog.load_table("multiengine.predictions").append(output)



    context.snowpark.sql("ALTER ICEBERG TABLE REVIEWS.PREDICTION REFRESH")

    return df
