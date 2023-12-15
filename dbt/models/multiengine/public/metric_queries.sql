{{ config(
    materialized='materializedview',
    pre_hook = "{{  create_source() }}",
    post_hook = "{{  create_sink() }}",
    tags=["risingwave"],
    group="risingwave"
    )
}}

with queries as (
    SELECT
        account_id,
        query_agent,
        start_time::timestamp as query_time,
        execution_duration_ms,
        processed_kb,
        round(processed_kb * execution_duration_ms / 10000000) as credits_consumed
    FROM source_queries
)
SELECT
    CONCAT(account_id, '-', query_agent, '-', window_start) as account_id_window_start,
    account_id,
    query_agent,
    window_start,
    window_end,
    count(*) as query_count,
    sum(execution_duration_ms) as sum_execution_duration_ms,
    sum(processed_kb) as sum_processed_kb,
    sum(credits_consumed) as sum_credits_consumed,
    max(query_time) as last_query_timestamp
FROM TUMBLE(queries, query_time, INTERVAL '1 day')
GROUP BY account_id, query_agent, window_start, window_end
