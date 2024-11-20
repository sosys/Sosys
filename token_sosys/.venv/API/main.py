from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import jwt
# from pydantic import BaseModel # Para receber body de PUT

# Chave secreta para gerar o token
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

# Banco de dados fictício para autenticação
fake_db = {
    "user1": "123",
    "user2": "111",
}

# Inicializando a aplicação FastAPI
app = FastAPI()

# Função para gerar o token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota para autenticação via GET
@app.get("/login")
async def login(username: str, password: str):
    # Verificação do usuário e senha
    if username in fake_db and fake_db[username] == password:
        access_token_expires = timedelta(minutes=1)
        access_token = create_access_token(
            data={"sub": username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Exemplo de uma rota protegida que requer autenticação
@app.get("/protected")
async def protected_route(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"message": f"Bem-vindo, {username}!"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
