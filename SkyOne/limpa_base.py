import pandas as pd
import json
import requests

def Get_API(headers, get_url, api_delete_url):
    
# Fazendo o GET para obter o JSON
    try:
        external_codes = []
        current_url = get_url
        page = '0'
        
        # Loop para processar páginas enquanto 'next_page' não for null
        while page != 'null':
            response = requests.get(current_url + page, headers=headers)
            response.raise_for_status()  # Lança exceção se o status for diferente de 200
            data = response.json()
            
            # Verifica se a chave 'data' está no JSON
            if 'data' not in data:
                print("Erro: JSON de resposta não contém a chave 'data'.")
                break
            
            external_codes = []
            
            # Adiciona os externalCodes da página atual
            page_external_codes = [item['id'] for item in data['data']]
            if len(page_external_codes) == 0:
                return 
            
            external_codes.extend(page_external_codes)
            print(f"External Codes coletados nesta página: {page_external_codes}")
            
            # Atualiza a URL para a próxima página
            #current_url = data.get('next_page')
            #print(f"Próxima página: {current_url}")
            #page = str(data['pagination'].get('next_page') - 1)
            #page = str(data['pagination'].get('next_page'))
            # Fazendo chamadas DELETE para cada externalCode coletado
            for code in external_codes:
                delete_url = api_delete_url + str(code)
                delete_response = requests.delete(delete_url, headers=headers)
                
                if delete_response.status_code == 204:
                    print(f"externalCode: {code}")
                else:
                    print(f"Falha ao deletar externalCode: {code}. Status: {delete_response.status_code}")        
        
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    except KeyError as e:
        print(f"Erro de chave: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

get_url_order = "https://v3.isa-api.com/api/v2/order-header/?user=SOSYS&skip="
get_url_item = "https://v3.isa-api.com/api/v2/order-item/?skip="
api_delete_url_order = "https://v3.isa-api.com/api/v2/order-header/"
api_delete_url_item = "https://v3.isa-api.com/api/v2/order-item/"
api_key = "ce668e73-7999-4e83-892b-c8c69e8c8d4e"

headers = {
            "Content-Type": "application/json",
            "apiKey": api_key  # Agora, a chave da API vai no cabeçalho como "api-key"
        }

#Get_API(headers, get_url_order, api_delete_url_order)    
Get_API(headers, get_url_item, api_delete_url_item)    

