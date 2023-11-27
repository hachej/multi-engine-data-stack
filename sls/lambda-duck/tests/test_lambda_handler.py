import boto3
import sys
import os
import pathlib
import datetime

sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

BUCKET_NAME = 'newsletter-multiengine-stack'

def test_my_model_save():
    os.environ['AWS_REGION'] = 'us-east-1'
    profile = "admin_aut_prod"
    session = boto3.Session(profile_name=profile)

    sts_client = session.client('sts')
    response = sts_client.get_session_token()

    access_key = response['Credentials']['AccessKeyId']
    secret_key = response['Credentials']['SecretAccessKey']
    session_token = response['Credentials']['SessionToken']

    os.environ["AWS_SESSION_TOKEN"] = session_token
    os.environ["AWS_ACCESS_KEY_ID"] = access_key
    os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key

    # test lambda handler
    from handler import handler
    limit = 20
    query = f"SELECT * FROM read_parquet('s3://{BUCKET_NAME}/data/tpch_1/year=*/month=*/*.parquet', HIVE_PARTITIONING = 1) WHERE year = 1992;"
    payload = {'q': query, 'limit': limit}
    output = handler(payload, {})

    d = (datetime.date(1992, 1, 1), datetime.date(1992, 1, 10))
    query = f"""
    SELECT strftime(L_SHIPDATE, '%Y-%m-%d') as day, sum(L_QUANTITY) as value
    FROM(
        SELECT *,year, month FROM read_parquet(f's3://{BUCKET_NAME}/data/tpch_1/year=*/month=*/*.parquet', HIVE_PARTITIONING = 1) as t
        WHERE (year > {d[0].year} OR (year = {d[0].year} AND month >= {d[0].month}))
        AND (year < {d[1].year} OR (year = {d[1].year} AND month <= {d[1].month}))
    )
    WHERE L_SHIPDATE >= '{d[0].strftime("%Y-%m-%d")}' AND L_SHIPDATE <= '{d[1].strftime("%Y-%m-%d")}'
    group by L_SHIPDATE;
    """
    payload = {'q': query, 'limit': limit}
    output = handler(payload, {})
