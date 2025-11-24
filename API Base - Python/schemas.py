from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

# Esquemas para autenticação
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="usuario123")
    email: EmailStr = Field(..., example="usuario@exemplo.com")
    full_name: Optional[str] = Field(None, max_length=100, example="Nome Completo")

    @field_validator('username', mode='after')
    @classmethod
    def validar_username(cls, v):
        """Valida que username não é apenas números e contém apenas caracteres permitidos."""
        if not v:
            raise ValueError("Nome de usuário não pode estar vazio")
        
        # Verifica se é apenas números
        if v.isdigit():
            raise ValueError("Nome de usuário não pode conter apenas números")
        
        # Verifica caracteres permitidos (letras, números, underscore, hífen, ponto)
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError("Nome de usuário pode conter apenas letras, números, underscore, hífen e ponto")
        
        return v

    @field_validator('full_name', mode='after')
    @classmethod
    def validar_full_name(cls, v):
        """Valida que full_name, se preenchido, contém apenas letras e espaços."""
        if v is None:
            return v
        
        if not v.strip():
            raise ValueError("Nome completo não pode estar vazio ou conter apenas espaços")
        
        # Permite letras (incluindo acentuadas), espaços, apóstrofos e hífens
        if not re.match(r'^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s\'-]+$', v):
            raise ValueError("Nome completo pode conter apenas letras, espaços, apóstrofos e hífens")
        
        return v.strip()

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="senhasegura123")

    @field_validator('password', mode='after')
    @classmethod
    def validar_password(cls, v):
        """Valida que a senha não é vazia e tem pelo menos 6 caracteres."""
        if not v:
            raise ValueError("Senha não pode estar vazia")
        
        if len(v) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
        
        return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    disabled: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    disabled: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Esquema para login
class LoginRequest(BaseModel):
    username: str = Field(..., example="usuario123")
    password: str = Field(..., example="senhasegura123")
