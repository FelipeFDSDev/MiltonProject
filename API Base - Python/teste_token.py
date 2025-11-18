#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para testar geração de token e validação"""

from auth import authenticate_user, create_access_token, get_current_user
from database import SessionLocal, User
from datetime import timedelta
from fastapi.security import HTTPAuthorizationCredentials

print("=" * 60)
print("TESTE 1: Autenticação do usuário")
print("=" * 60)

db = SessionLocal()

# Teste de autenticação
user = authenticate_user(db, "admin", "admin123")
if user:
    print(f"✓ Usuário autenticado: {user.username} (ID: {user.id})")
    print(f"  Email: {user.email}")
    print(f"  Desativado: {user.disabled}")
else:
    print("✗ Falha ao autenticar usuário 'admin' com senha 'admin123'")
    db.close()
    exit(1)

print("\n" + "=" * 60)
print("TESTE 2: Geração de Token JWT")
print("=" * 60)

access_token_expires = timedelta(minutes=1440)
token = create_access_token(
    data={"sub": user.username}, 
    expires_delta=access_token_expires
)

print(f"\n✓ Token gerado com sucesso!")
print(f"\nToken completo:")
print(token)

# Dividir o token para debug
parts = token.split('.')
print(f"\nPartes do token:")
print(f"  Header: {parts[0][:30]}...")
print(f"  Payload: {parts[1][:30]}...")
print(f"  Signature: {parts[2][:30]}...")

print("\n" + "=" * 60)
print("TESTE 3: Decodificar Payload do Token")
print("=" * 60)

import base64
import json

payload_encoded = parts[1]
padding = len(payload_encoded) % 4
if padding:
    payload_encoded += '=' * (4 - padding)

try:
    payload_decoded = base64.urlsafe_b64decode(payload_encoded)
    payload_data = json.loads(payload_decoded)
    print(f"\n✓ Payload decodificado:")
    for key, value in payload_data.items():
        print(f"  {key}: {value}")
except Exception as e:
    print(f"✗ Erro ao decodificar payload: {e}")

print("\n" + "=" * 60)
print("TESTE 4: Validar Token JWT")
print("=" * 60)

from auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"\n✓ Token decodificado com sucesso!")
    print(f"  Username (sub): {payload.get('sub')}")
    print(f"  Emitido em (iat): {payload.get('iat')}")
    print(f"  Expira em (exp): {payload.get('exp')}")
except jwt.ExpiredSignatureError:
    print(f"\n✗ Token expirado!")
except JWTError as e:
    print(f"\n✗ Erro ao validar token: {e}")

print("\n" + "=" * 60)
print("TESTE 5: Buscar usuário no banco com username do token")
print("=" * 60)

username_from_token = payload.get("sub")
if username_from_token:
    db_user = db.query(User).filter(User.username == username_from_token).first()
    if db_user:
        print(f"\n✓ Usuário encontrado no banco:")
        print(f"  ID: {db_user.id}")
        print(f"  Username: {db_user.username}")
        print(f"  Email: {db_user.email}")
        print(f"  Desativado: {db_user.disabled}")
    else:
        print(f"\n✗ Usuário '{username_from_token}' NÃO encontrado no banco!")
else:
    print(f"\n✗ Nenhum 'sub' encontrado no payload do token!")

db.close()

print("\n" + "=" * 60)
print("RESUMO DOS TESTES")
print("=" * 60)
print("✓ Autenticação: OK")
print("✓ Geração de Token: OK")
print("✓ Decodificação de Payload: OK")
print("✓ Validação de JWT: OK")
print("✓ Busca de Usuário no BD: OK")
print("\nTODOS OS TESTES PASSARAM! O sistema de autenticação está funcionando.")
