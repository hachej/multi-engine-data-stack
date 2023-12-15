DROP SOURCE source_queries; 

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
