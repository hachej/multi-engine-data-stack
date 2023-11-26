import boto3
import time
import json
import pandas as pd
import os


def invoke_lambda(json_payload_as_str: str, client):
    """
    Invoke our duckdb lambda function. Note that the payload is a string,
    so the method should be called with json.dumps(payload)
    """
    response = client.invoke(
        FunctionName='lambda-duck-dev-hello',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json_payload_as_str
    )

    # return response as dict
    return json.loads(response['Payload'].read().decode("utf-8"))


def fetch_query(query, client):
    start_time = time.time()
    response = invoke_lambda(json.dumps({'q': query}), client)
    roundtrip_time = int((time.time() - start_time) * 1000.0)

    if response.get("errorMessage", None):
        print(response)
        return None
    else:
        body = json.loads(response["body"])
        rows = body['data']['records']
        body['metadata']['roundtrip_time'] = roundtrip_time

        # return the results as a pandas dataframe and metadata
        return pd.DataFrame(rows), body['metadata']
