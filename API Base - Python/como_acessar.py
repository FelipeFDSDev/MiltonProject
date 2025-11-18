#!/usr/bin/env python3
"""
Exemplo de como acessar a API corretamente
"""

import requests

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("COMO ACESSAR A API COM AUTENTICAÇÃO")
print("=" * 70)

# Step 1: Gerar token
print("\n[1] Gerar token:")
print("    POST http://127.0.0.1:8000/auth/token")
print("    Body: username=admin&password=admin123")

response = requests.post(
    f"{BASE_URL}/auth/token",
    data={"username": "admin", "password": "admin123"}
)
token = response.json()['access_token']
print(f"    Token: {token[:50]}...\n")

# Step 2: Acessar com token
print("[2] Acessar /api/contacts/ COM Token:")
print(f"    GET http://127.0.0.1:8000/api/contacts/")
print(f"    Header: Authorization: Bearer {token[:30]}...")

headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{BASE_URL}/api/contacts/", headers=headers)
print(f"    Status: {response.status_code}")
print(f"    Response: {response.text}\n")

# Step 3: Comparar com acesso sem token
print("[3] Acessar /api/contacts/ SEM Token:")
print(f"    GET http://127.0.0.1:8000/api/contacts/")
print(f"    (sem header Authorization)")

response = requests.get(f"{BASE_URL}/api/contacts/")
print(f"    Status: {response.status_code}")
print(f"    Response: {response.text}\n")

print("=" * 70)
print("FORMAS DE ACESSAR:")
print("=" * 70)
print("""
1. SWAGGER UI (Recomendado):
   - Abra: http://127.0.0.1:8000/docs
   - Clique no botão "Authorize" (cadeado)
   - Cole o token gerado
   - Depois use as rotas normalmente

2. POSTMAN:
   - Method: GET
   - URL: http://127.0.0.1:8000/api/contacts/
   - Headers tab:
     Key: Authorization
     Value: Bearer {seu_token}

3. CURL:
   curl -H "Authorization: Bearer {seu_token}" http://127.0.0.1:8000/api/contacts/

4. NAVEGADOR (não funciona):
   - http://127.0.0.1:8000/api/contacts/
   - ❌ Vai retornar 401 porque navegador não envia header
""")
