from fastapi import FastAPI
from database import create_db_and_tables
from routes import contacts, mensagens, agendamentos
from dotenv import load_dotenv

# Importar todos os modelos para garantir que sejam registrados no Base.metadata
import models  # Isso garante que Cliente, HistoricoMensagem e MensagemAgendada sejam criados
from database import Contact  # Isso garante que Contact seja criado

load_dotenv()

app = FastAPI(
    title="Microserviço de Agendamento e Comunicação",
    description="Gerencia contatos, envio e agendamento de mensagens.",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    create_db_and_tables()

# Inclui rotas
app.include_router(contacts.router)
app.include_router(mensagens.router)
app.include_router(agendamentos.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Communication and Scheduling API"}

@app.post("/login", tags=["Autenticação"])
def login(username: str, password: str):
    """
    Faz login e retorna um token JWT.
    """
    if username == "admin" and password == "1234":
        token = criar_token(username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")