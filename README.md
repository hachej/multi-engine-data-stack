# Project setup

## Deploy the ingestion lambda function

```
cd setup/ingestion
sls plugin install -n serverless-better-credentials
sls plugin install -n serverless-iam-roles-per-function
sls deploy
```

## Setup data generator (shadowtraffic.io)

Create a free account at https://shadowtraffic.io/ and get a license.env file inside setup/shadowtraffic.

Get AWS session credentials.
```
export AWS_PROFILE=<your-profile>
aws sts get-session-token
```

Update the license.env file and add the AWS session credentials:

```bash
AWS_REGION=eu-central-1
AWS_ACCESS_KEY_ID=<access-key-id>
AWS_SECRET_ACCESS_KEY=<secret-access-key>
AWS_SESSION_TOKEN=<session-token>
```

## Setup glue catalog
````
cd setup/glue
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py
````

## Setup Snowflake catalog integration

Follow this Snowflage [guide](https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-external-volume-s3) to setup an external volume pointing to the S3 bucket.

## Setup SQLMesh

```
cd setup/glue
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.yaml.local config.yaml
```

Add your Snowflake credentials to the `config.yaml` file.

# Run the pipeline

Start shadowtraffic data generator:

```
cd setup/shadowtraffic

docker run --env-file license.env \
  -v $(pwd)/shadowtraffic.json:/home/config.json \
  shadowtraffic/shadowtraffic:latest \
  --config /home/config.json --watch \ 
```

Open another terminal and run SQLmesh.

```
sqlmesh --gateway duckdb plan
sqlmesh --gateway snowflake plan
```

# Question: 
## write enabled @IF... for python models ?

