#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para testar a API com requisição HTTP real"""

import requests
import json
from auth import create_access_token, authenticate_user
from database import SessionLocal
from datetime import timedelta

print("=" * 70)
print("TESTE: Requisição HTTP para a API")
print("=" * 70)

# Passo 1: Gerar token
db = SessionLocal()
user = authenticate_user(db, "admin", "admin123")

if not user:
    print("✗ Erro: Não foi possível autenticar usuário")
    db.close()
    exit(1)

access_token_expires = timedelta(minutes=1440)
token = create_access_token(
    data={"sub": user.username}, 
    expires_delta=access_token_expires
)
db.close()

print(f"\n✓ Token gerado: {token[:50]}...")

# Passo 2: Fazer requisição para a API
base_url = "http://127.0.0.1:8000"

print("\n" + "=" * 70)
print("TESTE 1: Requisição SEM token")
print("=" * 70)

headers_sem_token = {
    "Content-Type": "application/json"
}

try:
    response = requests.get(f"{base_url}/api/contacts", headers=headers_sem_token, timeout=5)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.ConnectionError:
    print("✗ ERRO: Não foi possível conectar à API")
    print("  A API está rodando em http://127.0.0.1:8000 ?")
except Exception as e:
    print(f"✗ ERRO: {e}")

print("\n" + "=" * 70)
print("TESTE 2: Requisição COM token no header")
print("=" * 70)

headers_com_token = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(f"{base_url}/api/contacts", headers=headers_com_token, timeout=5)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'Vazio'}")
except requests.exceptions.ConnectionError:
    print("✗ ERRO: Não foi possível conectar à API")
    print("  A API está rodando em http://127.0.0.1:8000 ?")
except Exception as e:
    print(f"✗ ERRO: {e}")

print("\n" + "=" * 70)
print("TESTE 3: Requisição para /test-auth")
print("=" * 70)

try:
    response = requests.get(f"{base_url}/test-auth", headers=headers_com_token, timeout=5)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'Vazio'}")
except requests.exceptions.ConnectionError:
    print("✗ ERRO: Não foi possível conectar à API")
    print("  A API está rodando em http://127.0.0.1:8000 ?")
except Exception as e:
    print(f"✗ ERRO: {e}")

print("\n" + "=" * 70)
print("TESTE 4: Requisição para /auth/me")
print("=" * 70)

try:
    response = requests.get(f"{base_url}/auth/me", headers=headers_com_token, timeout=5)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.json() if response.text else 'Vazio'}")
except requests.exceptions.ConnectionError:
    print("✗ ERRO: Não foi possível conectar à API")
    print("  A API está rodando em http://127.0.0.1:8000 ?")
except Exception as e:
    print(f"✗ ERRO: {e}")
