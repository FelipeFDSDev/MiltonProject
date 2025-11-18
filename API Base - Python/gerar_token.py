#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para gerar um novo token de teste"""

from auth import authenticate_user, create_access_token
from database import SessionLocal
from datetime import timedelta

db = SessionLocal()

# Tenta autenticar como admin
print("Tentando autenticar como 'admin'...")
user = authenticate_user(db, "admin", "admin123")

if not user:
    print("✗ ERRO: Não foi possível autenticar como 'admin'")
    print("Tentando com usuario123...")
    user = authenticate_user(db, "usuario123", "senha123")
    
    if not user:
        print("✗ ERRO: Nenhum usuário válido encontrado!")
        db.close()
        exit(1)

print(f"✓ Usuário autenticado: {user.username}")

# Gera o token
access_token_expires = timedelta(minutes=1440)
token = create_access_token(
    data={"sub": user.username}, 
    expires_delta=access_token_expires
)

print(f"\n{'='*70}")
print("TOKEN GERADO COM SUCESSO!")
print(f"{'='*70}")
print(f"\nToken (copie e cole sem aspas):\n{token}")

print(f"\n{'='*70}")
print("COMO USAR:")
print(f"{'='*70}")
print(f"\nEm curl:")
print(f"""curl -X 'GET' \\
  'http://127.0.0.1:8000/api/contacts/' \\
  -H 'accept: application/json' \\
  -H 'Authorization: Bearer {token}'""")

print(f"\nNo Swagger UI:")
print(f"1. Clique no botão cadeado (Authorize)")
print(f"2. Cole este token (sem 'Bearer', o Swagger adiciona):")
print(f"{token}")
print(f"3. Clique em 'Authorize'")
print(f"4. Clique em 'Close'")
print(f"5. Agora teste as rotas!")

db.close()
