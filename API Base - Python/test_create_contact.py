#!/usr/bin/env python3
"""
Gera token e cria um contato via JSON, depois lista contatos para confirmar.
"""
import requests
import json
import time

BASE = "http://127.0.0.1:8000"

# 1) gerar token
r = requests.post(f"{BASE}/auth/token", data={"username":"admin","password":"admin123"})
print("TOKEN STATUS:", r.status_code)
print(r.text)
if r.status_code != 200:
    print("Falha ao gerar token")
    raise SystemExit(1)

token = r.json().get('access_token')
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 2) criar contato (JSON)
contact = {
    "name": "Teste Usuario",
    "email": "teste.user+py@exemplo.com",
    "canalPref": "Whatsapp",
    "phone": "5511999888777",
    "codExterno": "TST-001"
}
print('\nCRIANDO CONTATO...')
rc = requests.post(f"{BASE}/api/contacts/", headers=headers, json=contact)
print('CREATE STATUS:', rc.status_code)
print(rc.text)

# 3) listar contatos para confirmar
print('\nLISTANDO CONTATOS...')
rlist = requests.get(f"{BASE}/api/contacts/", headers=headers)
print('LIST STATUS:', rlist.status_code)
print(rlist.text)
