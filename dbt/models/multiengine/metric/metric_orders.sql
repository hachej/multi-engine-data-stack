{{ config(
    materialized='table',
    description="Supabase table",
    pre_hook="{{ create_external_metabase_table('staging','staging_orders_per_month') }}", 
    tags=["supabase"]
    )
}}

SELECT
*
FROM {{ source('staging', 'staging_orders_per_month') }} 
