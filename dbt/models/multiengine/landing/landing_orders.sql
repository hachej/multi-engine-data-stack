

{{ config(
    materialized='table',
    description="Duck DB table",
    schema='landing',
    tags=["duckdb"]
    ) 
}}

SELECT * 
from {{ source('raw_data', 'orders') }} 
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY dt) = 1

