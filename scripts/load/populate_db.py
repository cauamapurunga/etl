import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.db import DatabaseConnector
import pandas as pd

db = DatabaseConnector(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres"
    )

for file in os.listdir("data/02-silver-validated"):
    if file.endswith(".parquet"):
        df = pd.read_parquet(f"data/02-silver-validated/{file}")

        db.create_table(
            file.replace(".parquet", ""),
            columns=[f"{col} TEXT" for col in df.columns]
        )

        db.insert_data(
            file.replace(".parquet", ""),
            df=df
        )