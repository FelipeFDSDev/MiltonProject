# validators.py
from pydantic import field_validator, ValidationError
import re
from typing import Any
from datetime import datetime

def validar_nome(nome: str) -> str:
    """Valida se o nome contém apenas letras, espaços e alguns caracteres especiais comuns."""
    if not re.match(r'^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s\'-]+$', nome):
        raise ValueError("O nome deve conter apenas letras, espaços e caracteres acentuados")
    return nome.strip()

def validar_telefone(telefone: str) -> str:
    """Valida o formato do telefone (apenas números, com ou sem DDD)."""
    if not telefone:
        return ""
        
    # Remove todos os caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    
    # Verifica se tem entre 10 e 11 dígitos (com DDD)
    if len(numeros) not in (10, 11):
        raise ValueError("Telefone deve conter 10 ou 11 dígitos (com DDD)")
    
    return numeros

def validar_codigo_externo(codigo: str) -> str:
    """Valida o código externo (letras, números e hífen/underscore)."""
    if not codigo:
        return ""
        
    if not re.match(r'^[a-zA-Z0-9_-]+$', codigo):
        raise ValueError("Código externo deve conter apenas letras, números, hífens ou underscores")
    return codigo

def validar_data_futura(data: datetime) -> datetime:
    """Valida se a data é futura."""
    if data <= datetime.now(data.tzinfo if data.tzinfo else None):
        raise ValueError("A data deve ser no futuro")
    return data

def validar_canal(canal: str) -> str:
    """Valida o canal de envio."""
    canal = canal.lower()
    if canal not in ["email", "whatsapp"]:
        raise ValueError("Canal inválido. Use 'email' ou 'whatsapp'")
    return canal
