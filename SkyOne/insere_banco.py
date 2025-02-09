import pandas as pd
import pyodbc

# Configuração da conexão com o SQL Server
server = 'localhost'  # Exemplo: 'localhost\SQLEXPRESS'
database = 'GUI_33'  # Nome do banco de dados
username = 'gui'  # Usuário do banco (se aplicável)
password = '123'  # Senha do banco (se aplicável)
driver = '{ODBC Driver 17 for SQL Server}'  # Verifique se o driver está instalado

# Criando a string de conexão
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Caminho do arquivo CSV
csv_file = 'C:\\bla\\CSV\\Order_Item.csv'  # Substitua pelo caminho do seu arquivo CSV

# Lendo o CSV com pandas
df = pd.read_csv(csv_file, sep=';', encoding='utf-8')

# Nome da tabela onde os dados serão inseridos
tabela_sql = 'ORDER_ITEM'

# Obtendo os nomes das colunas dinamicamente
colunas = df.columns.tolist()
placeholders = ', '.join(['?' for _ in colunas])  # "?, ?, ?, ?" conforme o número de colunas
colunas_sql = ', '.join(colunas)  # "coluna1, coluna2, coluna3"

# Montando a query de inserção
sql = f"INSERT INTO {tabela_sql} ({colunas_sql}) VALUES ({placeholders})"

# Iterando sobre as linhas do DataFrame e inserindo no banco
for _, row in df.iterrows():
    cursor.execute(sql, tuple(row))  # Converte a linha para uma tupla

# Confirmando a transação
conn.commit()

# Fechando a conexão
cursor.close()
conn.close()

print("Importação concluída com sucesso!")
