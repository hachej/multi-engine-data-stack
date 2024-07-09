
import os 
from pyiceberg.catalog import load_catalog
import pyarrow as pa
import pyarrow.json as paj
import boto3 
import json

# boto3
s3 = boto3.client('s3')

catalog = load_catalog("glue", **{"type": "glue",
                                "region_name":"eu-central-1",
                                "s3.region":"eu-central-1",
                        })

schema = pa.schema(
    [
        pa.field("reviewid", pa.string(), nullable=False),
        pa.field("username", pa.string(), nullable=False),
        pa.field("review", pa.string(), nullable=True),
        pa.field("ingestion_date", pa.int64(), nullable=False),
        pa.field("source_s3_key", pa.string(), nullable=False)
    ]
)

tables = catalog.list_tables("multiengine")
if ("multiengine", "landing_reviews") not in tables:
    print("Creating table")
    catalog.create_table(
        "multiengine.landing_reviews",
        schema=schema,
        location="s3://sumeo-parquet-data-lake/landing/reviews",
    )

iceberg_table = catalog.load_table("multiengine.landing_reviews")

def handler(event, context):
    for r in event["Records"]:
        bucket_name = r["s3"]["bucket"]["name"]
        key = r["s3"]["object"]["key"]
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        json_objects = [json.loads(line) | {"source_s3_key": key} for line in content.splitlines()]

    table = pa.Table.from_pylist(json_objects, schema=schema)
    iceberg_table.append(table)


if __name__ == "__main__":
    event= {
        "Records": [
            {
            "s3": {
                "bucket": {
                "name": "sumeo-parquet-data-lake",
                },
                "object": {
                    "key": "raw/reviews/part-1047589799372367.jsonl"
                }
            }
            }
        ]
        }
    handler(event, None)