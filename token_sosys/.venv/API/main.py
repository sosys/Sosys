from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from auth import validate_user, create_access_token, decode_access_token
import os

app = FastAPI()

# Modelo de entrada para autenticação
class TokenRequest(BaseModel):
    access_token: str
    secret_token: str

# Endpoint para tentar autenticar um acesso e gerar token
@app.post("/api/authenticate")
async def authenticate(request: TokenRequest):
    # Validar usuário
    try:
        validate_user(request.access_token, request.secret_token)
    except HTTPException as e:
        raise HTTPException(status_code=401, detail="Acesso nao autorizado")

    # Gerar token JWT
    token = create_access_token(data={"sub": request.access_token})
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) * 60
    }

# Configuração para extrair o token do cabeçalho Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/authenticate")

@app.get("/api/validate-token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    """
    Valida se o token enviado no cabeçalho Authorization ainda é válido.
    """
    try:
        payload = decode_access_token(token)
        return {"valid": True, "message": "Token is valid", "data": payload}
    except HTTPException as e:
        raise HTTPException(status_code=401, detail="erro ao validar token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado")