# models.py
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from validators import (
    validar_nome, 
    validar_telefone, 
    validar_codigo_externo, 
    validar_data_futura,
    validar_canal
)
import re

# --- Pydantic Models (Entrada/Saída da API) ---
# ----------------------------------------------

# Modelo base para criar/atualizar um Contato (Payload de entrada)
class ContactBase(BaseModel):
    name: str = Field(..., example="João Silva")
    email: EmailStr = Field(..., example="joao.silva@empresa.com")
    canalPref: str = Field(..., example="Whatsapp")
    phone: Optional[str] = Field(None, example="5511999998888")
    codExterno: Optional[str] = Field(None, example="A0013")

    # Validações
    @field_validator('name', mode='after')
    @classmethod
    def validar_nome_contato(cls, v):
        """Valida que nome não é apenas números."""
        if not v or not v.strip():
            raise ValueError("Nome do contato não pode estar vazio")
        
        # Verifica se é apenas números
        if re.sub(r'\D', '', v) == v and v.isdigit():
            raise ValueError("Nome do contato não pode conter apenas números")
        
        return validar_nome(v)

    @field_validator('phone', mode='after')
    @classmethod
    def validar_telefone_contato(cls, v):
        if v is None:
            return v
        return validar_telefone(v)

    @field_validator('codExterno', mode='after')
    @classmethod
    def validar_codigo_externo_contato(cls, v):
        if v is None:
            return v
        return validar_codigo_externo(v)

    @field_validator('canalPref', mode='after')
    @classmethod
    def validar_canal_pref_contato(cls, v):
        return validar_canal(v)

# Modelo completo de Contato (Payload de resposta)
# NOTE: Sem validações para evitar erros ao serializar dados antigos
class Contact(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="João Silva")
    email: str = Field(..., example="joao.silva@empresa.com")
    phone: Optional[str] = Field(None, example="5511999998888")
    codExterno: Optional[str] = Field(None, example="A0013")
    canalPref: str = Field(..., example="email")
    cliente_id: Optional[int] = None

    class Config:
        from_attributes = True  # Necessário para conversão ORM → Pydantic


# ---- Modelos de Cliente (para a API) ----
class ClienteBase(BaseModel):
    nome: str = Field(..., example="Empresa XPTO")
    email: EmailStr = Field(..., example="contato@empresa.com")
    telefone: Optional[str] = Field(None, example="11988887777")

    @field_validator('nome', mode='after')
    @classmethod
    def validar_nome_cliente(cls, v):
        """Valida que nome não é apenas números."""
        if not v or not v.strip():
            raise ValueError("Nome do cliente não pode estar vazio")
        
        if re.sub(r'\D', '', v) == v and v.isdigit():
            raise ValueError("Nome do cliente não pode conter apenas números")
        
        return validar_nome(v)

    @field_validator('telefone', mode='after')
    @classmethod
    def validar_telefone_cliente(cls, v):
        if v is None:
            return v
        return validar_telefone(v)

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
    contact_id: int = Field(..., gt=0, description="ID do contato que receberá a mensagem")
    canal: str = Field(..., example="email", description="Canal de envio: email ou whatsapp")
    assunto: Optional[str] = Field(None, example="Lembrete Importante")
    conteudo: str = Field(..., example="Sua consulta está agendada para amanhã.")
    data_agendamento: datetime = Field(..., example="2025-11-23T14:30:00", description="Data e hora para envio")

    @field_validator('canal', mode='after')
    @classmethod
    def validar_canal_mensagem(cls, v):
        return validar_canal(v)

    @field_validator('data_agendamento', mode='after')
    @classmethod
    def validar_data_agendamento(cls, v):
        return validar_data_futura(v)

    @field_validator('assunto', mode='after')
    @classmethod
    def validar_assunto(cls, v):
        if v is not None and len(v) > 200:
            raise ValueError("O assunto não pode ter mais de 200 caracteres")
        return v

    @field_validator('conteudo', mode='after')
    @classmethod
    def validar_conteudo(cls, v):
        if not v.strip():
            raise ValueError("O conteúdo da mensagem não pode estar vazio")
        if len(v) > 2000:
            raise ValueError("A mensagem não pode ter mais de 2000 caracteres")
        return v

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
