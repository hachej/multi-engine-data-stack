import streamlit as st
import pandas as pd
import numpy as np
from utils import fetch_query
import nivo_chart as nc
import datetime   
import boto3
import os 

S3_BASE_PATH = "s3://newsletter-multiengine-stack/data/tpch_1/"
session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"])
lambda_client = session.client('lambda', region_name='us-east-1')

d = st.date_input(
    "Sales analytics date range",
    (datetime.date(1995, 1, 1),datetime.date(1995, 1, 10)),
    datetime.date(1992, 1, 1),
    datetime.date(1998, 12, 31),
    format="MM.DD.YYYY",
)
     
d

query = f"""
    SELECT strftime(L_SHIPDATE, '%Y-%m-%d') as day, sum(L_QUANTITY) as value
    FROM(
        SELECT *,year, month FROM read_parquet('{S3_BASE_PATH}/year=*/month=*/*.parquet', HIVE_PARTITIONING = 1) as t
        WHERE (year > {d[0].year} OR (year = {d[0].year} AND month >= {d[0].month}))
        AND (year < {d[1].year} OR (year = {d[1].year} AND month <= {d[1].month}))
    )
    WHERE L_SHIPDATE >= '{d[0].strftime("%Y-%m-%d")}' AND L_SHIPDATE <= '{d[1].strftime("%Y-%m-%d")}'
    group by L_SHIPDATE;
    """
df, metadata = fetch_query(query, lambda_client)

# st.write(f"Total row count: {df['C'][0]}")
st.write(f"Roundtrip time: {metadata['roundtrip_time']}ms")
st.write(f"Query exec. time: {metadata['timeMs']} ms")

layout= {
    "title": "Quantity shipped per day",
    "type": "calendar",
    "height": 800,
    "width": 1000,
    "from": df["day"].min(), # "1992-01-01
    "to": df["day"].max(),
    "emptyColor": "#eeeeee",
    "colors": ["#61cdbb", "#97e3d5", "#e8c1a0", "#f47560"],
    "margin": {"top": 40, "right": 40, "bottom": 40, "left": 40},
    "yearSpacing": 40,
    "monthBorderColor": "#ffffff",
    "dayBorderWidth": 2,
    "dayBorderColor": "#ffffff",
    "legends": [
        {
            "anchor": "bottom-right",
            "direction": "row",
            "translateY": 36,
            "itemCount": 4,
            "itemWidth": 42,
            "itemHeight": 36,
            "itemsSpacing": 14,
            "itemDirection": "right-to-left",
        }
    ],
}

df["value"]=df["value"].astype(int)
df["day"]=df["day"].astype(str)
nc.nivo_chart(data=df.to_dict('records'), layout=layout, key="calendar_chart")