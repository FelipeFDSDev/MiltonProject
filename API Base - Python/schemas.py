from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

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

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="senhasegura123")

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
