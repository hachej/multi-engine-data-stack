{{ config(
    materialized='table',
    description="Supabase table",
    group="supabase",
    tags=["supabase"]
    )
}}

SELECT
    account_id::uuid as account_id,
    churn_probability,
    prediction_date::date
FROM {{ source('staging', 'account_churn') }} 