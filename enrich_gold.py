import pandas as pd
from db import DatabaseConnector

db = DatabaseConnector(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="postgres"
)

with open("03-gold-enriched/query.sql", "r", encoding="utf-8") as f:
    query = f.read()

cursor = db.conn.cursor()
cursor.execute(query)
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
cursor.close()

df_enriched = pd.DataFrame(results, columns=columns)

df_enriched.to_parquet("03-gold-enriched/users_enriched.parquet", index=False)
df_enriched.to_csv("03-gold-enriched/users_enriched.csv", index=False, encoding="utf-8")

print(f"Registros processados: {len(df_enriched)}")
print(f"\nEstados: {df_enriched['uf'].nunique()}")
print(f"\nDistribuição por gênero:")
print(df_enriched['genero'].value_counts())

db.close()