from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import BaseHTTPMiddleware

# Importar rotas
from routes import contacts, mensagens, agendamentos
from routers import auth
from database import create_db_and_tables
from auth import get_current_active_user

app = FastAPI(
    title="Microserviço de Agendamento e Comunicação",
    description="Gerencia contatos, envio e agendamento de mensagens.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "syntaxHighlight.theme": "obsidian",
        "tryItOutEnabled": True,
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 1,
        "filter": True,
        "showCommonExtensions": True,
    },
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Configuração do esquema de segurança
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Insira o token JWT (o prefixo 'Bearer ' será adicionado automaticamente)"
        }
    }
    
    # Adiciona segurança global a todas as rotas, exceto as de autenticação
    if "paths" in openapi_schema:
        for path, methods in openapi_schema["paths"].items():
            # Pula rotas de autenticação e documentação
            if path in ["/auth/token", "/auth/register", "/docs", "/redoc", "/openapi.json", "/", "/health"]:
                continue
                
            for method_name, method in methods.items():
                if isinstance(method, dict):
                    # Pula o método OPTIONS (usado para CORS)
                    if method_name.lower() == "options":
                        continue
                    # Adiciona segurança a todos os métodos da rota
                    if "security" not in method:
                        method["security"] = [{"bearerAuth": []}]
    
    # Adiciona segurança global
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Middleware para debug (verificar se o token está sendo enviado)
class DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log de todas as requisições
        print("\n===== REQUISIÇÃO RECEBIDA =====")
        print(f"Método: {request.method}")
        print(f"URL: {request.url}")
        print(f"Cabeçalhos: {dict(request.headers)}")
        
        # Verifica se há token no header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            print(f"DEBUG: Token encontrado no header: {auth_header}")
            
            # Se o token começar com 'Bearer ', tenta decodificá-lo para debug
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
                parts = token.split('.')
                if len(parts) == 3:  # Um JWT válido tem 3 partes
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
                        print(f"DEBUG: Conteúdo do token (debug): {payload_data}")
                    except Exception as e:
                        print(f"DEBUG: Não foi possível decodificar o token para debug: {e}")
        else:
            print(f"DEBUG: Nenhum token encontrado para {request.method} {request.url.path}")
        
        # Processa a requisição
        response = await call_next(request)
        
        print(f"Status da resposta: {response.status_code}")
        print("===== FIM DA REQUISIÇÃO =====\n")
        return response

# Adiciona middleware de debug (ativar temporariamente para debug)
app.add_middleware(DebugMiddleware)

# Configuração do CORS
# Configurado para permitir todas as origens (desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por uma lista de origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Inclui rotas da API
app.include_router(auth.router, tags=["authentication"])
app.include_router(contacts.router, prefix="/api", tags=["Contatos"])
app.include_router(mensagens.router, prefix="/api", tags=["Mensagens"])
app.include_router(agendamentos.router, prefix="/api", tags=["Agendamentos"])

# Rota de health check
@app.get("/health")
async def health_check():
    """Verifica se a API está online."""
    return {
        "status": "ok",
        "service": "Communication and Scheduling API",
        "version": "1.0.0"
    }

# Rota de teste de autenticação
@app.get("/test-auth")
async def test_auth(current_user = Depends(get_current_active_user)):
    """Rota de teste para verificar se a autenticação está funcionando."""
    return {
        "status": "authenticated",
        "username": current_user.username,
        "email": current_user.email,
        "message": "Autenticação funcionando corretamente!"
    }

# Rota raiz
@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "Communication and Scheduling API",
        "documentation": "/docs"
    }

# Evento de inicialização
@app.on_event("startup")
async def startup():
    # Garante que as tabelas estejam criadas
    create_db_and_tables()