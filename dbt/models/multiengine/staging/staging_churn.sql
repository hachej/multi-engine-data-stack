{{ config(
    materialized='external', 
    location="s3://{{ env_var('BUCKET_NAME') }}/data/staging/churn/churn.parquet",
    format="parquet",
    description="Duck DB table",
    group='duckdb',
    tags=["duckdb"]
    )
}}

SELECT
    account_id::BLOB as account_id,
    random() as churn_probability,
    current_date::VARCHAR::BLOB as prediction_date
FROM {{ ref('landing_accounts') }} 