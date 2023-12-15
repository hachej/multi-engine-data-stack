{% macro create_sink() %}
    {% set query %}
    CREATE SINK target_count_postgres_sink FROM metric_queries WITH (
        connector = 'jdbc',
        jdbc.url = '{{ env_var("SUPABASE_JDBC_CONNECTION_STRING") }}',
        table.name = 'query_metrics',
        type = 'upsert',
        primary_key = 'account_id_window_start'
    );
    {% endset %}
    {% do run_query(query) %}

{% endmacro %}


{% macro create_source() %}
    {% set query %}
        CREATE SOURCE IF NOT EXISTS source_queries (
        query_id varchar,
        account_id varchar,
        query_agent varchar,
        start_time varchar,
        processed_kb float,
        compute_size float,
        execution_duration_ms float
        )
        WITH (
        connector='kafka',
        topic='query-topic',
        properties.bootstrap.server='host.docker.internal:29092',
        scan.startup.mode='latest',
        scan.startup.timestamp_millis='140000000'
        ) FORMAT PLAIN ENCODE JSON;
    {% endset %}
    {% do run_query(query) %}

{% endmacro %}