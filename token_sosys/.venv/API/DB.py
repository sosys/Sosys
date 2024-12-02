import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente
load_dotenv()

# Configurações do Banco
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# Pool de conexões com o banco de dados
connection_pool = pool.SimpleConnectionPool(
    1,  # Mínimo de conexões
    10, # Máximo de conexões
    **DB_CONFIG
)

def get_connection():
    """Obtém uma conexão do pool"""
    try:
        return connection_pool.getconn()
    except Exception as e:
        raise RuntimeError("Erro ao obter conexão do banco de dados") from e

def release_connection(connection):
    """Libera uma conexão de volta ao pool"""
    connection_pool.putconn(connection)

def close_all_connections():
    """Fecha todas as conexões do pool"""
    connection_pool.closeall()

def create_client_db(nome: str, cnpj: str, access_token: str, secret_token: str, ativo: str, deletado: str):
    try:
        # Obtendo uma conexão do pool
        connection = get_connection()
        cursor = connection.cursor()
        
        # Verificar se o CNPJ já existe
        cursor.execute("SELECT 1 FROM clientes WHERE cnpj = %s", (cnpj,))
        if cursor.fetchone():
            raise ValueError("CNPJ já existe no banco de dados")
        
        # Inserir o novo cliente
        insert_query = """
            INSERT INTO clientes (nome, cnpj, access_token, secret_token, ativo, deletado)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        cursor.execute(insert_query, (nome, cnpj, access_token, secret_token, ativo, deletado))
        
        # Obter o ID do cliente criado
        client_id = cursor.fetchone()[0]
        
        # Commit na transação
        connection.commit()
        
        return {"id": client_id, "nome": nome, "cnpj": cnpj}
    
    except Exception as e:
        # Em caso de erro, faz o rollback da transação
        connection.rollback()
        raise RuntimeError(f"Erro ao criar cliente: {e}")
    
    finally:
        # Fechar o cursor e liberar a conexão
        cursor.close()
        release_connection(connection)