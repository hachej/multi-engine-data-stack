CREATE SINK target_count_postgres_sink FROM metric_queries WITH (
    connector = 'jdbc',
    jdbc.url = 'jdbc:postgresql://db.iiawsxgmdjqdqzorpwqh.supabase.co:5432/postgres?user=postgres&password=posF_jptkvx4pDC2haj_koFJ',
    table.name = 'query_metrics',
    type = 'upsert',
    primary_key = 'account_id_window_start'
);