import pandas as pd
import json
import requests


def AlfaNum(cNumero):
    nValor    = 0
    lSoNumero = True
    nAtual    = 0
    cAscii    = ""
    nPosIni   = 0
    cCaract   = ""
    nValAux   = 0
    cZeros    = ""
    cNumero = cNumero.upper()
     
    #Percorre os valores
    for nAtual in range(len(cNumero)):
        cCaract = cNumero[nAtual]
        
        # Se encontrar uma letra
        if cCaract.isalpha():
            if nPosIni == 0:
                nPosIni = nAtual
            lSoNumero = False
            break  # Interrompe o loop ao encontrar uma letra
     
    #Se tiver somente numero, converte com Val
    if lSoNumero:
        nValor = int(cNumero)
    else:
        nValor = 0
         
        #Percorre os valores
        for nAtual in range(len(cNumero)):
            cCaract = cNumero[nAtual]
            cZeros = "0" * (len(cNumero) - nAtual - 1)
        
            # Se tiver alguma letra no número
            if cCaract.isalpha():
                # Converte a letra para número
                cAscii = str(ord(cCaract) - 64 + 9)  # Converte letra para número
                
                # Se for a partir da segunda posição e não for a última
                if nAtual > nPosIni and nAtual != len(cNumero) - 1:
                    nValAux = int(cAscii + cZeros) + (ord(cCaract) - 64) * 26
                    nValAux *= int(cAscii)
                    nValAux += (26 + int(cAscii))
                    nValor += nValAux
                else:
                    nValor += int(cAscii + cZeros) + (ord(cCaract) - 64) * 26
            # Se for somente números
            else:
                # Se for a partir da segunda posição e não for a última
                if nAtual > nPosIni and nAtual != len(cNumero) - 1:
                    nValor += int(cCaract + cZeros) + (36 * 26) + (26 * int(cCaract))
                else:
                    nValor += int(cCaract + cZeros)
    return nValor

def read_csv_and_send_in_batches(csv_file_path, api_url, api_key):
    batch_size = 100
    # Ler o arquivo CSV
    try:
        df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')
        print(f"Arquivo CSV lido com sucesso! {len(df)} registros encontrados.")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return
    
    # Garantir que a coluna 'C5_EMISSAO' seja tratada como data e formatar para 'YYYY-MM-DD'
    df['C5_EMISSAO'] = pd.to_datetime(df['C5_EMISSAO'], errors='coerce').dt.strftime('%Y-%m-%d')
        
    # Mapeamento dos campos para o formato desejado
    formatted_data = []
    for _, row in df.iterrows():        
        if isinstance(row['C6_QTDVEN'], str): 
            qtd = float(row['C6_QTDVEN'].replace(',', '.'))
        else:
            qtd = row['C6_QTDVEN']
            
        formatted_data.append({
            "cost": row['D2_CUSTO1'],
            "user": "SOSYS",
            "price": float(row['C6_PRUNIT'].replace(',', '.')),
            "quantity": qtd,
            "product": str(row['B1_COD']),
            "order": AlfaNum(row['C5_NUM'])
        })
    
    # Particionar os dados em chunks de 'batch_size'
    for i in range(0, len(formatted_data), batch_size):
        batch = formatted_data[i:i + batch_size]
        
        # Converter o batch para JSON sem quebras de linha e sem indentação
        body_json = json.dumps(batch)
        print(f"Enviando lote {i // batch_size + 1} com {len(batch)} linhas...")
        
        # Enviar a requisição
        headers = {
            "Content-Type": "application/json",
            "apiKey": api_key  # Agora, a chave da API vai no cabeçalho como "api-key"
        }
        response = requests.post(api_url, data=body_json, headers=headers)

        if response.status_code == 201:
            print(f"Lote {i // batch_size + 1} enviado com sucesso! Resposta: {response.text}")
        else:
            #print(f"Erro ao enviar lote {i // batch_size + 1}. Status Code: {response.status_code}")
            #print("Body enviado:", body_json)
            print("Resposta da API:", response.text)
            
csv_file_path = 'C:\\bla\\faturamento.csv'  # Substitua com o caminho correto do seu arquivo CSV
api_url = "https://v3.isa-api.com/api/v2/order-item/bulk"  # Substitua com a URL da sua API
api_key = "ce668e73-7999-4e83-892b-c8c69e8c8d4e"

# Enviar os dados em lotes de 50
read_csv_and_send_in_batches(csv_file_path, api_url, api_key)    

