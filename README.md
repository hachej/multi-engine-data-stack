# Multi Engine Data Stacks

Experimentations around mixing compute engine together for building data platforms.

# Distribution Layer
Setup of a very simple distribution layer based on duckDB and AWS Lambda.

## sls/

Contains lambda function code.

Replace with your bucket name in file sls/lambda-duck/serverless.yml row 24.

Deploy with:
```
cd sls/lambda-duck
export AWS_PROFILE=<your_profile>
sls deploy
```

## streamlit/
Contains streamlit dashboard.

Replace BUCKET_NAME variable with your bucket name in file streamlit/app.py

run locally with:
```
cd streamlit
export AWS_PROFILE=<your_profile>
streamlit run app.py
```

# Data Pipeline Layer
Setup of a very simple multi engine data stack.

More details in [this](https://juhache.substack.com/p/multi-engine-data-stack-v0) article: 

1- Install requirements.txt
```
pip install -r requirements.txt
```

2- Replace BUCKET_NAME by your bucket name in the following files:
- dbt/models/sources.yml
- dbt/models/multiengine/landing/landing_orders.sql
- dagster_assets/__init__.py

3- Set the following env variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

4- Set your dbt/profiles.yml
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

5- Setup Snowflake:
```
CREATE DATABASE NEWSLETTER_MULTIENGINE_STACK;

CREATE OR REPLACE STORAGE INTEGRATION NEWSLETTER_MULTIENGINE_STACK_INTEGRATION
...;

CREATE OR REPLACE FILE FORMAT NEWSLETTER_MULTIENGINE_STACK_FORMAT
  TYPE = PARQUET
;

CREATE OR REPLACE STAGE NEWSLETTER_MULTIENGINE_STACK_STAGE
  STORAGE_INTEGRATION = NEWSLETTER_MULTIENGINE_STACK_INTEGRATION
  URL = ...
  FILE_FORMAT = NEWSLETTER_MULTIENGINE_STACK_FORMAT;
```

6- Run Dagster
```
dagster dev
```


