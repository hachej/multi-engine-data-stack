-- {% macro create_external_metabase_table(schema_name, table_name) %}
-- {% if execute %}
--     {% set query %}
--         CREATE SCHEMA IF NOT EXISTS {{schema_name}};
--     {% endset %}
--     {% do run_query(query) %}

--     {% set check_table_exists_query %}
--     SELECT * FROM information_schema.tables 
--     WHERE  table_schema = '{{ schema_name }}' and table_name  = '{{ table_name }}'
--     {% endset %} 

--     {% set results = run_query(check_table_exists_query) %}

--     {% if results|length > 0 %}
--         {{ print("drop external table ") }} 
--         {% set query %}
--             DROP FOREIGN TABLE {{ schema_name }}.{{ table_name }};
--         {% endset %}
--         {% do run_query(query) %}
--     {% endif %}

--     {{ print("create external table ") }}
--     {% set create_external_table_query %}
--         CREATE FOREIGN TABLE {{ schema_name }}.{{ table_name }} (
--             account_id varchar,
--             churn_probability float,
--             prediction_date date
--         )
--         server
--         s3_server
--             options (
--             uri 's3://newsletter-multiengine-stack/data/staging/churn/churn.parquet',
--             format 'parquet'
--         );
--     {% endset %}
--     {% print(create_external_table_query) %} 
--     {% set results = run_query(create_external_table_query) %}
-- {% endif %}
-- {% endmacro %}