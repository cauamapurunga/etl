import os
import pandas as pd

class DataNormalizer:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def convert_columns_to_strings(self, df):
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
        return df 
    
    def load_df_from_file(self, file, ext):
        input_path = os.path.join(self.input_dir, file)

        if ext.lower() == ".csv":
            df = pd.read_csv(input_path)
        elif ext.lower() == ".json":
            try:
                df = pd.read_json(input_path)
            except ValueError:
                df = pd.read_json(input_path, lines=True)
        return df

    def normalize_data(self):   
        for file in os.listdir(self.input_dir):
            name, ext = os.path.splitext(file)
            output_path = os.path.join(self.output_dir, f"{name}.parquet")

            df = self.load_df_from_file(file, ext)

            df = self.convert_columns_to_strings(df)
            
            # Remove registros com erro da API (específico para cep_info)
            if 'erro' in df.columns:
                df = df[df['erro'] != 'true']
                df = df.drop('erro', axis=1)
            
            df = df.drop_duplicates().reset_index(drop=True)
            df.to_parquet(output_path, index=False)

if __name__ == "__main__":
    input_directory = "data/01-bronze-raw"
    output_directory = "data/02-silver-validated"

    normalizer = DataNormalizer(input_directory, output_directory)
    normalizer.normalize_data()