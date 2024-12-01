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
