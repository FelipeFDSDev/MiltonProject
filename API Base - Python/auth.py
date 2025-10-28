# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

# Configurações do token (fixas para testes)
SEGREDO_JWT = "MiltonProject"
ALGORITMO = "HS256"

# Instância do esquema de segurança
seguranca = HTTPBearer()

# Função para criar token JWT
def criar_token(username: str):
    return jwt.encode({"sub": username}, SEGREDO_JWT, algorithm=ALGORITMO)

# Função para verificar token JWT
def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(seguranca)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SEGREDO_JWT, algorithms=[ALGORITMO])
        return payload["sub"]  # retorna o nome do usuário
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
