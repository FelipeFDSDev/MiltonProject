#!/usr/bin/env python3
"""
Gera token e chama /api/mensagens/enviar/ com canal=email para testar envio.
"""
import requests

BASE = "http://127.0.0.1:8000"

# 1) gerar token
r = requests.post(f"{BASE}/auth/token", data={"username":"admin","password":"admin123"})
print("TOKEN STATUS:", r.status_code)
print(r.text)
if r.status_code != 200:
    print("Falha ao gerar token")
    raise SystemExit(1)

token = r.json().get('access_token')
headers = {"Authorization": f"Bearer {token}"}

# 2) enviar mensagem via email
params = {
    'canal': 'email',
    'destinatario': 'felipefrs2007@gmail.com',
    'conteudo': 'TESTE',
    'assunto': 'TESTE'
}
print('\nENVIANDO MENSAGEM...')
resp = requests.post(f"{BASE}/api/mensagens/enviar/", headers=headers, params=params)
print('STATUS:', resp.status_code)
print('RESP:', resp.text)
