import requests
import pandas as pd

def get_data(cep):
    endpoint = f"https://viacep.com.br/ws/{cep}/json/"

    response = requests.get(endpoint)
    cep_info = response.json()
    
    return cep_info

users_path = "01-bronze-raw/users.csv"
users_df = pd.read_csv(users_path)
print(users_df.head())

cep_lists = users_df['cep'].tolist()

for cep in cep_lists:
    data = get_data(cep)
    print(data)