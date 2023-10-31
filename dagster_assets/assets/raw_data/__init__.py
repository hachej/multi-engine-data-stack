import numpy as np
import pandas as pd
from dagster import asset
from dagster_assets.assets.raw_data.duckpond import SQL
from dagster_assets.utils import random_data


@asset(compute_kind="random")
def orders() -> SQL:
    """A table containing all orders that have been placed."""
    df= random_data(
        extra_columns={"order_id": str, "quantity": int, "purchase_price": float, "sku": str},
        n=10000,
    )
    # generate duplicates
    duplicated_orders = df[0:10].copy()
    duplicated_orders["quantity"] = duplicated_orders["quantity"] + 10
    df = pd.concat([df, duplicated_orders])
    return SQL("select * from $df", df=df)
