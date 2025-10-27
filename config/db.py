import os
import pandas as pd
import psycopg2

class DatabaseConnector:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def create_table(self, table_name, columns):
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")
        self.conn.commit()
        cursor.close()

    def insert_data(self, table_name, df):
        cursor = self.conn.cursor()
        for index, row in df.iterrows():
            placeholders = ', '.join(['%s'] * len(row))
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", tuple(row))
        self.conn.commit()
        cursor.close()

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def select_all_data_from_table(self, table_name, limit=10):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def close(self):
        self.conn.close()
