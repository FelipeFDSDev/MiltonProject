#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar se o registro de usuário está funcionando com pbkdf2_sha256.
"""
import requests
import json
import sys
from datetime import datetime, timedelta
from jose import jwt

BASE_URL = "http://127.0.0.1:8000"
SECRET_KEY = "milton_project_2023_secret_key"
ALGORITHM = "HS256"

def criar_token_admin():
    """Cria um token JWT válido para o usuário admin."""
    now = datetime.utcnow()
    expire = now + timedelta(minutes=60)
    
    payload = {
        "sub": "admin",
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp())
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def testar_registro():
    """Testa o endpoint POST /auth/register."""
    print("\n" + "="*60)
    print("TESTANDO REGISTRO DE NOVO USUÁRIO")
    print("="*60)
    
    # Cria token admin
    admin_token = criar_token_admin()
    print(f"\n[1] Token Admin criado: {admin_token[:30]}...")
    
    # Dados do novo usuário
    timestamp = int(__import__('time').time())
    novo_usuario = {
        "username": f"usuario_teste_{timestamp}",
        "password": "SenhaTesteMuito@Forte123!@#$%^&*()",  # Senha longa para testar pbkdf2
        "email": f"teste_{timestamp}@example.com",
        "full_name": "Usuário Teste Novo"
    }
    
    print(f"\n[2] Registrando novo usuário:")
    print(f"   - username: {novo_usuario['username']}")
    print(f"   - email: {novo_usuario['email']}")
    print(f"   - password length: {len(novo_usuario['password'])} caracteres")
    
    # Faz o request
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=novo_usuario,
            headers=headers,
            timeout=10
        )
        
        print(f"\n[3] Response Status: {response.status_code}")
        print(f"    Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"\n[OK] SUCESSO! Usuário registrado:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"\n[ERRO] ERRO! Status {response.status_code}")
            try:
                print(f"Response Body: {response.json()}")
            except:
                print(f"Response Body (text): {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n[ERRO] ERRO: Não foi possível conectar ao servidor em {BASE_URL}")
        print("   Certifique-se de que o uvicorn está rodando!")
        return False
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_login():
    """Testa se consegue fazer login com a nova senha."""
    print("\n" + "="*60)
    print("TESTANDO LOGIN COM NOVO USUÁRIO")
    print("="*60)
    
    credenciais = {
        "username": "usuario_teste_novo",
        "password": "SenhaTesteMuito@Forte123!@#$%^&*()"
    }
    
    print(f"\n[1] Tentando fazer login:")
    print(f"   - username: {credenciais['username']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data=credenciais,
            timeout=10
        )
        
        print(f"\n[2] Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n[OK] LOGIN BEM-SUCEDIDO!")
            print(f"   Token: {data.get('access_token', '')[:30]}...")
            print(f"   Type: {data.get('token_type')}")
            return True
        else:
            print(f"\n[ERRO] LOGIN FALHOU! Status {response.status_code}")
            try:
                print(f"Response: {response.json()}")
            except:
                print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n[AVISO] Servidor não está respondendo. Pulando teste de login.")
        return None
    except Exception as e:
        print(f"\n[ERRO] ERRO inesperado: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "[TEST] TESTANDO CORRECAO DO REGISTRO COM pbkdf2_sha256")
    
    registro_ok = testar_registro()
    
    if registro_ok:
        print("\n[AGUARDE] Aguardando 1 segundo antes de testar login...")
        import time
        time.sleep(1)
        login_ok = testar_login()
        
        if login_ok:
            print("\n" + "="*60)
            print("[OK] TODOS OS TESTES PASSARAM COM SUCESSO!")
            print("="*60)
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("[AVISO] Registro funcionou mas login falhou")
            print("="*60)
            sys.exit(1)
    else:
        print("\n" + "="*60)
        print("[ERRO] TESTE FALHOU NO REGISTRO")
        print("="*60)
        sys.exit(1)
