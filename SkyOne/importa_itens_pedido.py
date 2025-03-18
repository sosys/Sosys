import pandas as pd
import json
import requests

def read_csv_and_send_in_batches(csv_file_path, api_url, api_key):
    batch_size = 100
    # Ler o arquivo CSV
    try:
        df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')
        print(f"Arquivo CSV lido com sucesso! {len(df)} registros encontrados.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return
    
    BASE_URL = "https://v3.isa-api.com/api/v2/order-item"
    headers = {
        "Content-Type": "application/json",
        "apiKey": api_key  # Agora, a chave da API vai no cabeçalho como "api-key"
    }
    
    formatted_data = []
    for _, row in df.iloc[205165:].iterrows():
        formatted_data.append({
            "cost": float(row['cost'].replace(',', '.')),
            "user": row["uusers"],
            "price": float(row['price'].replace(',', '.')),
            "quantity": float(row['quantity'].replace(',', '.')),
            "product": row['product'].strip(),
            "order": row['oorder']
        })
                
        response = requests.post(api_url, data=json.dumps(formatted_data), headers=headers)

        if response.status_code == 201:
            print(row['oorder'] + ' - ' + row['product'])
            print("Resposta da API:", response.text)
        else:
            print('certo: ' + str(row['ID']))

csv_file_path = 'C:\\bla\\CSV\\Order_Item_GIGS.csv'  # Substitua com o caminho correto do seu arquivo CSV
api_url = "https://v3.isa-api.com/api/v2/order-item/bulk"  # Substitua com a URL da sua API
api_key = "ce668e73-7999-4e83-892b-c8c69e8c8d4e"

# Enviar os dados em lotes de 50
read_csv_and_send_in_batches(csv_file_path, api_url, api_key)   #226262 

