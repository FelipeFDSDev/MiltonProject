from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import User, SessionLocal

# Configurações do JWT
SECRET_KEY = "milton_project_2023_secret_key"
ALGORITHM = "HS256"
# Aumentando o tempo de expiração para 24 horas (1440 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Configuração para hash de senhas
# Usa `bcrypt_sha256` primeiro to support passwords longer than 72 bytes.
# `bcrypt_sha256` hashes the password with SHA-256 first, then bcrypt, avoiding
# the 72-byte limitation of raw bcrypt for arbitrary-length passwords.
pwd_context = CryptContext(
    # Prioriza pbkdf2_sha256 (pure-Python, sem dependência de bcrypt C-extension),
    # depois bcrypt_sha256 e bcrypt para compatibilidade com hashes antigos.
    schemes=["pbkdf2_sha256", "bcrypt_sha256", "bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)

# Modelo de dados do token
class TokenData(BaseModel):
    username: Optional[str] = None

# Configuração do esquema de autenticação
# Usando HTTPBearer para permitir inserir token manualmente no Swagger UI
http_bearer = HTTPBearer(scheme_name="bearerAuth", auto_error=False)

# Mantém OAuth2PasswordBearer para a rota de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    if not plain_password or not hashed_password:
        return False
    
    try:
        # Let passlib handle verification. It will select the correct handler
        # (bcrypt_sha256 or bcrypt) based on the stored hash prefix.
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # If passlib fails (very unlikely), fall back to manual bcrypt check.
        try:
            import bcrypt
            password_bytes = plain_password.encode('utf-8')
            # bcrypt only supports 72 bytes; truncate bytes safely for direct check
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            hash_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False

# Função para criar hash da senha
def get_password_hash(password: str) -> str:
    """Cria um hash da senha fornecida."""
    try:
        # Prefer using the configured pwd_context (bcrypt_sha256 first).
        # bcrypt_sha256 avoids the 72-byte limit by hashing with SHA-256 first.
        return pwd_context.hash(password)
    except Exception as e:
        # As a last-resort fallback, try the explicit bcrypt_sha256 hasher.
        try:
            from passlib.hash import bcrypt_sha256
            return bcrypt_sha256.hash(password)
        except Exception as fallback_e:
            print(f"Erro ao criar hash da senha: {e} | fallback error: {fallback_e}")
            raise

# Função para autenticar usuário
def authenticate_user(db: Session, username: str, password: str):
    """Autentica um usuário verificando username e senha."""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Função para criar token de acesso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    print("\n===== CRIAÇÃO DE TOKEN =====")
    print(f"DEBUG: Dados iniciais do token: {data}")
    
    # Cria uma cópia dos dados para não modificar o dicionário original
    to_encode = data.copy()
    
    # Define o tempo de expiração
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # Converte para timestamp (número) para o JWT
    expire_timestamp = int(expire.timestamp())
    iat_timestamp = int(datetime.utcnow().timestamp())
    
    # Adiciona o tempo de expiração ao payload (deve ser timestamp, não datetime)
    to_encode.update({"exp": expire_timestamp, "iat": iat_timestamp})
    
    print(f"DEBUG: Payload final do token: {to_encode}")
    print(f"DEBUG: Chave secreta: {SECRET_KEY}")
    print(f"DEBUG: Algoritmo: {ALGORITHM}")
    
    try:
        # Gera o token JWT
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        print(f"DEBUG: Token gerado: {encoded_jwt}")
        print("===== FIM DA CRIAÇÃO DE TOKEN =====\n")
        return encoded_jwt
    except Exception as e:
        print(f"ERRO ao gerar token: {e}")
        raise

# Função para obter o usuário atual a partir do token
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
) -> User:
    """
    Extrai e valida o token JWT da requisição.
    O token deve estar no header: Authorization: Bearer <token>
    """
    print("\n===== INÍCIO DA VALIDAÇÃO DO TOKEN =====")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais. Por favor, faça login novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        print("ERRO: Nenhum token fornecido")
        raise credentials_exception
    
    # Extrai o token das credenciais e remove aspas extras se houver
    token = credentials.credentials
    # Remove aspas duplas e simples do início e fim
    token = token.strip('"').strip("'")
    print(f"DEBUG: Token recebido: {token[:20]}... (comprimento: {len(token)} caracteres)")
    
    try:
        
        # Verifica se o token tem o formato correto
        parts = token.split('.')
        if len(parts) != 3:
            print(f"ERRO: Formato de token inválido. Partes encontradas: {len(parts)}")
            raise credentials_exception
        
        # Tenta decodificar o payload para debug
        try:
            import base64
            import json
            
            # Decodifica o payload (parte do meio)
            payload_encoded = parts[1]
            # Adiciona padding se necessário
            padding = len(payload_encoded) % 4
            if padding:
                payload_encoded += '=' * (4 - padding)
            
            payload_decoded = base64.urlsafe_b64decode(payload_encoded)
            payload_data = json.loads(payload_decoded)
            print(f"DEBUG: Conteúdo do token: {payload_data}")
            
            # Verifica se o token tem um campo 'sub' (subject/usuário)
            if 'sub' not in payload_data:
                print("ERRO: Token não contém 'sub' (usuário)")
                raise credentials_exception
                
        except Exception as e:
            print(f"AVISO: Não foi possível decodificar o payload do token: {e}")
        
        # Tenta decodificar o token com verificação
        try:
            print("DEBUG: Tentando decodificar o token com a chave secreta...")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print("DEBUG: Token decodificado com sucesso!")
            
            username: str = payload.get("sub")
            if not username:
                print("ERRO: Nenhum username encontrado no token após decodificação")
                raise credentials_exception
            
            print(f"DEBUG: Usuário do token: {username}")
            
            # Obtém o usuário do banco de dados
            db = SessionLocal()
            try:
                print(f"DEBUG: Buscando usuário '{username}' no banco de dados...")
                user = db.query(User).filter(User.username == username).first()
                
                if user is None:
                    print(f"ERRO: Usuário '{username}' não encontrado no banco de dados")
                    raise credentials_exception
                
                # Verifica se o token está expirado
                expire = payload.get("exp")
                if not expire:
                    print("ERRO: Token não contém data de expiração")
                    raise credentials_exception
                
                expire_dt = datetime.fromtimestamp(expire)
                now = datetime.utcnow()
                
                print(f"DEBUG: Token expira em: {expire_dt} (UTC)")
                print(f"DEBUG: Hora atual: {now} (UTC)")
                
                if now > expire_dt:
                    print("ERRO: Token expirado")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Sessão expirada. Por favor, faça login novamente.",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                print("DEBUG: Token válido e não expirado")
                print(f"DEBUG: Autenticação bem-sucedida para o usuário: {user.username}")
                print("===== FIM DA VALIDAÇÃO DO TOKEN =====\n")
                return user
                
            except Exception as e:
                print(f"ERRO ao acessar o banco de dados: {e}")
                raise credentials_exception
                
            finally:
                db.close()
                
        except jwt.ExpiredSignatureError:
            print("ERRO: Token expirado (ExpiredSignatureError)")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão expirada. Por favor, faça login novamente.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        except JWTError as e:
            print(f"ERRO ao decodificar token (JWTError): {e}")
            print(f"DEBUG: SECRET_KEY sendo usada: {SECRET_KEY}")
            print(f"DEBUG: ALGORITMO sendo usado: {ALGORITHM}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido. Por favor, faça login novamente.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except Exception as e:
        print(f"ERRO inesperado durante a validação do token: {e}")
        import traceback
        print("Traceback:", traceback.format_exc())
        raise credentials_exception

# Função para verificar se o usuário está ativo
async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

# Função para verificar se o usuário é administrador
async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    # Por enquanto, todos os usuários têm permissão de admin
    # Você pode adicionar um campo is_admin na tabela User se necessário
    return current_user
