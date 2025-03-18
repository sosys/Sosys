import pandas as pd

def csv_to_parquet(csv_file: str, parquet_file: str):
    try:
        df = pd.read_csv(csv_file, delimiter=";", encoding="utf-8", low_memory=False)
        df.to_parquet(parquet_file, engine='pyarrow', index=True)
        print(f"Arquivo Parquet salvo em: {parquet_file}")
        
        df = pd.read_parquet(parquet_file)
        print(df.head())  # Verificar as primeiras linhas do dataframe
    except Exception as e:
        print(f"Erro ao converter CSV para Parquet: {e}" + ' - ' + csv_file)


path_de = "C:\\bla\\CSV\\"
path_para = "C:\\bla\\Parquet\\"

nome_csv_order = 'Order_Header.csv'
nome_parquet_order = "order_header.parquet"

nome_csv_item = 'Order_Item.csv'
nome_parquet_item = "order_item.parquet"

nome_csv_wallet = 'wallet.csv'
nome_parquet_wallet = "wallet.parquet"

nome_csv_client = 'client.csv'
nome_parquet_client = "client.parquet"

nome_csv_product = 'product_sb1.csv'
nome_parquet_product = "product_sb11.parquet"

# Exemplo de uso
#csv_to_parquet(path_de + nome_csv_order, path_para + nome_parquet_order)
#csv_to_parquet(path_de + nome_csv_item, path_para + nome_parquet_item)

#csv_to_parquet(path_de + nome_csv_wallet, path_para + nome_parquet_wallet)
#csv_to_parquet(path_de + nome_csv_client, path_para + nome_parquet_client)
csv_to_parquet(path_de + nome_csv_product, path_para + nome_parquet_product)