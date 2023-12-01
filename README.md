Setup of a very simple multi engine data stack.

More details in [this](https://juhache.substack.com/p/multi-engine-data-stack-v0) article: 

# Getting Started

1- Install requirements.txt
```
pip install -r requirements.txt
```


1- Set the following variables in the .env file:
rename .env.local to .env and complete the following variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- BUCKET_NAME

2- Set your dbt/profiles.yml
```
duck:
  target: duck
  outputs:
    duck:
      type: duckdb
      path: dbt.duckdb
      extensions:
        - httpfs
        - parquet
      settings:
        s3_region:
        s3_access_key_id: 
        s3_secret_access_key: 

supabase:
  target: supabase
  outputs: 
    supabase:
      type: postgres
      host: 
      user: postgres
      password: 
      port: 5432
      dbname: postgres
      schema: metric
      threads: 1
      connect_timeout: 30

snow: 
  target: snow
  outputs: 
    snow:
      type: snowflake
      account: 
      user: 
      password: 
      database:
      schema: 
```

3- Run Dagster
```
dagster dev
```


