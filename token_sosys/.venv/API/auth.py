from datetime import datetime, timedelta
from fastapi import HTTPException
from argon2 import PasswordHasher, exceptions
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from DB import get_connection, release_connection
import os
from dotenv import load_dotenv

load_dotenv()
CHAVE_JWT = os.getenv("CHAVE_JWT")
ALGORITHM = "HS256"
TEMPO_DO_TOEKN = int(os.getenv("TEMPO_DO_TOEKN"))
DB_CHAVE_DEV = os.getenv("DB_CHAVE_DEV")

# Função para validar credenciais
def validate_user(access_token: str, secret_token: str):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Consultar cliente no banco
        cursor.execute("""
            SELECT secret_token
            FROM clientes
            WHERE pgp_sym_decrypt(access_token::bytea, %s) = %s
              AND ativo = 'S'
              AND deletado = 'N';
        """, (DB_CHAVE_DEV, access_token))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=401, detail="Access_token invalido")

        stored_hash = result[0]

        # Validar secret_token com Argon2
        ph = PasswordHasher()
        try:
            ph.verify(stored_hash, secret_token)
            return True
        except exceptions.VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Secret_token invalido")

    finally:
        cursor.close()
        release_connection(connection)

# Função para gerar o token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TEMPO_DO_TOEKN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, CHAVE_JWT, algorithm=ALGORITHM)

# Decodifica e valida token JWT
def decode_access_token(token: str):
    """
    Decodifica e valida o token JWT.
    """
    try:
        payload = jwt.decode(token, CHAVE_JWT, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirou")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalido")