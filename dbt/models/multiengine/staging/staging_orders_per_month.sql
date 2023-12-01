{{ config(
    materialized='external', 
    location="s3://{{ env_var('BUCKET_NAME') }}/data/staging/orders_per_month/orders_per_month.parquet",
    format="parquet",
    description="Duck DB table",
    tags=["duckdb"]
    )
}}
WITH month_extracted AS (
    SELECT
        month(dt) AS month,
        year( dt) AS year,
        quantity
    FROM {{ ref('landing_orders') }} 
)
SELECT 
    month,
    year,
    COUNT(*) AS total_orders_per_month,
    SUM(quantity) AS total_quantity_per_month
FROM month_extracted
GROUP BY year, month
