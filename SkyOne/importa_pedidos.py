import pandas as pd
import json
import requests

def read_csv_and_send_in_batches(csv_file_path, api_url, api_key):
    batch_size = 1
    # Ler o arquivo CSV
    try:
        df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')
        print(f"Arquivo CSV lido com sucesso! {len(df)} registros encontrados.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return
    
    BASE_URL = "https://v3.isa-api.com/api/v2/order-header/external/"
    headers = {
        "Content-Type": "application/json",
        "apiKey": api_key  # Agora, a chave da API vai no cabeçalho como "api-key"
    }
    
    formatted_data = []
    for _, row in df.iloc[16760:].iterrows():
        url = f"{BASE_URL}{row["externalCode"]}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if 'id' not in response.text:
                print(row["externalCode"])
                formatted_data = ([{
                    "date": row["ddate"],
                    "status": row["sstatus"],
                    "client": str(row["client"]),
                    "user": row["uuser"],
                    "externalCode": row["externalCode"]
                }])
                
                response = requests.post(api_url, data=json.dumps(formatted_data), headers=headers)

                if response.status_code != 201:
                    print("Body enviado:", formatted_data)
                    print("Resposta da API:", response.text)
    # Particionar os dados em chunks de 'batch_size'
    #for i in range(0, len(formatted_data), batch_size):
    #    batch = formatted_data[i:i + batch_size]
    #    
    #    # Converter o batch para JSON sem quebras de linha e sem indentação
    #    body_json = json.dumps(batch)
    #    print(f"Enviando lote {i // batch_size + 1} com {len(batch)}  linhas de {len(formatted_data)}...")
    #    
    #    # Enviar a requisição
    #    response = requests.post(api_url, data=body_json, headers=headers)

        
            
csv_file_path = 'C:\\bla\\CSV\\Order_Header.csv'  # Substitua com o caminho correto do seu arquivo CSV
api_url = "https://v3.isa-api.com/api/v2/order-header/bulk"  # Substitua com a URL da sua API
api_key = "ce668e73-7999-4e83-892b-c8c69e8c8d4e"

# Enviar os dados em lotes de 50
read_csv_and_send_in_batches(csv_file_path, api_url, api_key)    

