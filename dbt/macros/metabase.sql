{% macro create_external_metabase_table(schema_name, table_name) %}
{% if execute %}
    {% set query %}
        CREATE SCHEMA IF NOT EXISTS {{schema_name}};
    {% endset %}
    {% do run_query(query) %}

    {% set check_table_exists_query %}
    SELECT * FROM information_schema.tables 
    WHERE  table_schema = '{{ schema_name }}' and table_name  = '{{ table_name }}'
    {% endset %} 

    {% set results = run_query(check_table_exists_query) %}

    {% if results|length > 0 %}
        {{ print("drop external table ") }} 
        {% set query %}
            DROP FOREIGN TABLE {{ schema_name }}.{{ table_name }};
        {% endset %}
        {% do run_query(query) %}
    {% endif %}

    {{ print("create external table ") }}
    {% set create_external_table_query %}
        CREATE foreign table {{ schema_name }}.{{ table_name }} (
            month bigint,
            year bigint,
            total_orders_per_month bigint,
            total_quantity_per_month float
        )
        server
        s3_server
            options (
            uri 's3://newsletter-multiengine-stack/data/staging/orders_per_month/orders_per_month.parquet',
            format 'parquet'
        );
    {% endset %}

    {% set results = run_query(create_external_table_query) %}
{% endif %}
{% endmacro %}