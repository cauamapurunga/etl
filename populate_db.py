from db import DatabaseConnector
import pandas as pd
import os

db = DatabaseConnector(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres"
    )

for file in os.listdir("02-silver-validated"):
    if file.endswith(".parquet"):
        df = pd.read_parquet(f"02-silver-validated/{file}")

        db.create_table(
            file.replace(".parquet", ""),
            columns=[f"{col} TEXT" for col in df.columns]
        )

        db.insert_data(
            file.replace(".parquet", ""),
            df=df
        )