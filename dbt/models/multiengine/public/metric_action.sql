{{ config(
    materialized='view',
    description="Supabase table",
    tags=["supabase"],
    group="supabase"
    )
}}

SELECT 
    c.account_id,
    churn_probability,
    prediction_date,
    m.query_count,
    CASE WHEN churn_probability > 0.5 OR query_count > 10 THEN 1 ELSE 0 END as display_churn_action
FROM {{ ref("metric_churn") }}  as c
JOIN {{ source("metric", "query_metrics") }} as m
on c.account_id = m.account_id
and m.query_agent = 'chatbot'
and m.window_start = current_date
