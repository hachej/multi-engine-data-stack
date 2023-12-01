import pandas as pd
import random
import duckdb
from datetime import datetime
from utils import random_data
import os 
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class DataGenerator:
    def __init__(self, bucket, prefix) -> None:
        self.bucket = bucket
        self.prefix = prefix
        self.db = duckdb.connect(":memory:")

        self.db.query(f"""install httpfs;
                    load httpfs;
                    set s3_region="us-east-1";
                    set s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
                    set s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
                    """)

    def _get_s3_url(self, id):
        timestamp_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        return f"s3://{self.bucket}/{self.prefix}{id}/{timestamp_str}.parquet"

    def generate(self, df: pd.DataFrame, id: str):
        url = self._get_s3_url(id)
        print(url)
        self.db.query(f"COPY (SELECT * FROM df) to '{url}' (FORMAT PARQUET)")

# connect to an in-memory database
generator = DataGenerator(
    bucket=os.environ["BUCKET_NAME"],
    prefix="data/"
)

# generate random data
df= random_data(
    extra_columns={"order_id": str, "quantity": int, "purchase_price": float, "sku": str},
    n = random.randint(10, 11)
)
# generate duplicates
duplicated_orders = df[0:10].copy()
duplicated_orders["quantity"] = duplicated_orders["quantity"] + 10
df = pd.concat([df, duplicated_orders])

generator.generate(df, "raw_data/orders")
