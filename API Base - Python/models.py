# models.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# --- Pydantic Models (Entrada/Saída da API) ---
# ----------------------------------------------

# Modelo base para criar/atualizar um Contato (Payload de entrada)
class ContactBase(BaseModel):
    name: str = Field(..., example="João Silva")
    email: EmailStr = Field(..., example="joao.silva@empresa.com")
    canalPref: str = Field(..., example="Whatsapp")
    phone: Optional[str] = Field(None, example="5511999998888")
    codExterno: Optional[str] = Field(None, example="A0013")

# Modelo completo de Contato (Payload de resposta)
class Contact(ContactBase):
    id: int = Field(..., example=1)
    cliente_id: Optional[int] = None

    class Config:
        from_attributes = True  # Necessário para conversão ORM → Pydantic


# ---- Modelos de Cliente (para a API) ----
class ClienteBase(BaseModel):
    nome: str = Field(..., example="Empresa XPTO")
    email: EmailStr = Field(..., example="contato@empresa.com")
    telefone: Optional[str] = Field(None, example="11988887777")

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int
    criado_em: datetime
    contatos: List[Contact] = []
    
    class Config:
        from_attributes = True


# ---- Modelos de Histórico de Mensagem (para a API) ----
class HistoricoBase(BaseModel):
    canal: str = Field(..., example="email")
    destinatario: str = Field(..., example="cliente@teste.com")
    conteudo: str = Field(..., example="Sua entrega foi confirmada.")
    status: Optional[str] = Field("PENDENTE", example="ENVIADO")

class HistoricoOut(HistoricoBase):
    id: int
    data_envio: datetime
    
    class Config:
        from_attributes = True


# ---- Modelos de Mensagem Agendada (para a API) ----
class MensagemAgendadaCreate(BaseModel):
    canal: str = Field(..., example="email", description="Canal de envio: email ou whatsapp")
    destinatario: str = Field(..., example="cliente@teste.com")
    assunto: Optional[str] = Field(None, example="Lembrete Importante")
    conteudo: str = Field(..., example="Sua consulta está agendada para amanhã.")
    data_agendamento: datetime = Field(..., example="2025-11-03T14:30:00", description="Data e hora para envio")

class MensagemAgendadaUpdate(BaseModel):
    canal: Optional[str] = None
    destinatario: Optional[str] = None
    assunto: Optional[str] = None
    conteudo: Optional[str] = None
    data_agendamento: Optional[datetime] = None
    status: Optional[str] = None

class MensagemAgendadaOut(BaseModel):
    id: int
    canal: str
    destinatario: str
    assunto: Optional[str]
    conteudo: str
    data_agendamento: datetime
    status: str
    criado_em: datetime
    enviado_em: Optional[datetime]
    erro_mensagem: Optional[str]
    
    class Config:
        from_attributes = True


# --- Modelo de Usuário para Autenticação ---
class UserBase(BaseModel):
    username: str = Field(..., example="usuario123")
    email: EmailStr = Field(..., example="usuario@exemplo.com")
    full_name: Optional[str] = Field(None, example="Nome Completo")
    disabled: Optional[bool] = Field(False, example=False)

class UserCreate(UserBase):
    password: str = Field(..., example="senhasegura123")

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelo para token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
