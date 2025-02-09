import pyodbc

# Configurações de conexão com o SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=GUI_33;'
    'UID=gui;'
    'PWD=123'
)

# Função para executar os updates a partir de uma linha inicial até uma linha final
def executar_updates(txt_file, linha_inicial, linha_final):
    cursor = conn.cursor()

    try:
        updates_batch = []  # Lista para armazenar as instruções de update em lote
        
        with open(txt_file, mode='r') as file:
            # Itera sobre o arquivo com index para localizar a linha inicial e final
            for index, line in enumerate(file, start=1):
                # Se a linha for menor que a linha inicial, ignora
                if index < linha_inicial:
                    continue
                
                # Se a linha for maior que a linha final, para de processar
                if index > linha_final:
                    break
                
                sql_query = line.strip()  # Remove espaços extras ou nova linha
                if sql_query:  # Certifica-se de que a linha não está vazia
                    updates_batch.append(sql_query)
                    
                    # Se o lote atingir um tamanho específico, executa o batch
                    if len(updates_batch) >= 1000:  # Limite de 1000 instruções por vez (ajuste conforme necessário)
                        cursor.execute('; '.join(updates_batch))
                        print(f"Executando em lote: {updates_batch}")
                        updates_batch = []  # Limpa o lote após execução

            # Executa o último lote (caso haja instruções restantes)
            if updates_batch:
                cursor.execute('; '.join(updates_batch))
                print(f"Executando em lote final: {updates_batch}")

            # Confirma as alterações após processar todas as instruções
            conn.commit()

    except Exception as e:
        print(f"Erro ao executar as instruções: {e}")
        conn.rollback()  # Caso haja erro, reverte as alterações

    finally:
        cursor.close()

# Chama a função passando o caminho para o seu arquivo TXT e as linhas inicial e final
txt_file = 'C:\\bla\\novo 19.txt'  # Substitua pelo caminho do seu arquivo TXT
linha_inicial = 10000  # Defina a linha a partir da qual começar (ex: linha 10)
linha_final = 500000    # Defina a linha até a qual processar (ex: linha 15)
executar_updates(txt_file, linha_inicial, linha_final)

# Fecha a conexão
conn.close()

