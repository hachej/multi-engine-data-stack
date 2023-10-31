

{{ config(
    materialized='external', 
    location='s3://newsletter-multiengine-stack/data/landing_orders/landing_orders.parquet',
    format="parquet",
    tags=["duckdb"]
    ) 
}}
SELECT * 
from {{ source('raw_data', 'orders') }} 
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY dt) = 1

