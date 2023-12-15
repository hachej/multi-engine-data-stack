{{ config(
    materialized='view',
    description="Supabase table",
    tags=["supabase"],
    group="supabase"
    )
}}
with sub as (
SELECT 
    account_id, 
    subscription_id, 
    subscription_start_date, 
    credits_purchased
FROM {{ source("metric", "subscriptions") }} 
where current_date between subscription_start_date::date and subscription_end_date::date
)
select 
    sub.account_id, 
    sub.subscription_id, 
    sub.subscription_start_date, 
    credits_purchased,
    credits_purchased / 30 as credits_purchased_daily,
    m.window_start as consumption_date,
    m.sum_credits_consumed as credits_consumed_daily,
    m.sum_processed_kb as sum_processed_kb_daily,
    m.sum_execution_duration_ms as sum_execution_duration_ms_daily,
    sum(m.sum_credits_consumed) OVER (PARTITION BY sub.account_id, sub.subscription_id
                         ORDER BY m.window_start) AS credits_consumed_cumulative

from sub
LEFT JOIN {{ source("metric", "query_metrics") }} as m
ON m.account_id = sub.account_id 
and m.query_agent = 'chatbot' 
and m.window_start >= sub.subscription_start_date
order by account_id, subscription_id, consumption_date




