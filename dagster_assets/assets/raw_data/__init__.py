import numpy as np
import pandas as pd
from dagster import asset
from dagster_assets.assets.raw_data.duckpond import SQL
from dagster_assets.utils import _random_times
import uuid
import random
import datetime
import lorem

@asset(compute_kind="random")
def accounts() -> SQL:
    """A table containing all orders that have been placed."""
    dataset_size = 1000
 
    data = {
        "account_id": ["c4cefa9e-8a45-45be-ae65-5a1d3972e18e", "dcf134a1-1871-49d5-8fdf-64fd82c907cf"],
        "country": [ "FR", "US"],
        "age":  np.random.randint(2, 50, size=2) ,
        "dt" : [datetime.datetime.now(), datetime.datetime.now()]
    }

    df = pd.DataFrame(data)
    # generate duplicates
    duplicates = df[0:2].copy()
    df = pd.concat([df, duplicates])
    return SQL("select * from $df", df=df)
