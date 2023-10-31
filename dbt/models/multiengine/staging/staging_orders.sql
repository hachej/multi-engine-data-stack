{{ config(
    materialized='table', 
    tags=["snowflake"],
    pre_hook="{{ dbt_external_tables.stage_external_sources('landing.landing_orders') }}"
    )
}}

WITH month_extracted as (
    SELECT
        TO_TIMESTAMP_NTZ(to_timestamp_ntz(dt)) AS dt_datetime,
        MONTH(dt_datetime) as month,
        YEAR(dt_datetime) as year,
        quantity
    FROM {{ source('landing', 'landing_orders') }} 
)
SELECT 
    month,
    year,
    count(*) as total_orders_per_month,
    sum(quantity) as total_quantity_per_month
from month_extracted
group by year, month