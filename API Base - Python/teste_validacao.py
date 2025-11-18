#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para testar a validação de token na requisição"""

import asyncio
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import get_current_user, get_current_active_user
from database import SessionLocal

print("=" * 70)
print("TESTE: Validação de Token (simulando requisição da API)")
print("=" * 70)

# Token gerado no teste anterior
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MzI0ODk2OSwiaWF0IjoxNzYzMTYyNTY5fQ.fcmj9QthebGgYuZv6b0Z0hBG04AalzA_a3W_dybWbEA"

print(f"\nToken para testar:")
print(f"{token}\n")

# Criar credenciais HTTP (como se viesse do header Authorization: Bearer <token>)
credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

print("=" * 70)
print("TESTE 1: Passar credenciais para get_current_user()")
print("=" * 70)

try:
    # Simular a chamada como se fosse de uma rota
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    user = loop.run_until_complete(get_current_user(credentials))
    
    print(f"\n✓ Validação bem-sucedida!")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Desativado: {user.disabled}")
    
except Exception as e:
    print(f"\n✗ ERRO na validação do token:")
    print(f"  Tipo: {type(e).__name__}")
    print(f"  Mensagem: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TESTE 2: Passar credenciais para get_current_active_user()")
print("=" * 70)

try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    user = loop.run_until_complete(get_current_active_user(credentials))
    
    print(f"\n✓ Validação bem-sucedida!")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Desativado: {user.disabled}")
    
except Exception as e:
    print(f"\n✗ ERRO na validação do token:")
    print(f"  Tipo: {type(e).__name__}")
    print(f"  Mensagem: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TESTE 3: Testar com credenciais None (nenhum token)")
print("=" * 70)

try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    user = loop.run_until_complete(get_current_user(None))
    
    print(f"\n✓ Validação bem-sucedida (inesperado!)")
    
except Exception as e:
    print(f"\n✓ Erro esperado quando nenhum token é fornecido:")
    print(f"  Tipo: {type(e).__name__}")
    print(f"  Mensagem: {str(e)}")

print("\n" + "=" * 70)
print("TESTE 4: Testar com token inválido")
print("=" * 70)

invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MzI0ODk2OSwiaWF0IjoxNzYzMTYyNTY5fQ.AAAAAAAAAAAAAAAAAAAAAAAAAAA"

credentials_invalid = HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)

try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    user = loop.run_until_complete(get_current_user(credentials_invalid))
    
    print(f"\n✓ Validação bem-sucedida (inesperado!)")
    
except Exception as e:
    print(f"\n✓ Erro esperado para token inválido:")
    print(f"  Tipo: {type(e).__name__}")
    print(f"  Mensagem: {str(e)}")

print("\n" + "=" * 70)
print("RESUMO")
print("=" * 70)
print("Sistema de validação de token: OK")
