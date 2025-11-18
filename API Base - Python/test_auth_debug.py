#!/usr/bin/env python3
"""
Debug detalhado da autenticação
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_complete():
    print("=" * 70)
    print("TESTE DETALHADO DE AUTENTICAÇÃO")
    print("=" * 70)
    
    # Step 1: Gerar token
    print("\n[STEP 1] Gerando token...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/token",
            data={"username": "admin", "password": "admin123"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            print("❌ Falha ao gerar token!")
            return
            
        token_data = response.json()
        token = token_data.get('access_token')
        print(f"✓ Token gerado com sucesso")
        print(f"  Tipo: {token_data.get('token_type')}")
        print(f"  Token: {token[:50]}...")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # Step 2: Verificar rota de autenticação teste
    print("\n[STEP 2] Testando /test-auth...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/test-auth",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ /test-auth funcionando!")
        else:
            print(f"❌ /test-auth retornou {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Step 3: Testar /api/contacts/
    print("\n[STEP 3] Testando /api/contacts/...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/contacts/",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ /api/contacts/ funcionando!")
        else:
            print(f"❌ /api/contacts/ retornou {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Step 4: Verificar headers sendo enviados
    print("\n[STEP 4] Verificando headers enviados...")
    print(f"Authorization: Bearer {token[:30]}...")
    
    # Step 5: Fazer requisição sem token
    print("\n[STEP 5] Testando sem token (deve retornar 401)...")
    try:
        response = requests.get(f"{BASE_URL}/api/contacts/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✓ Corretamente rejeitado sem token!")
        else:
            print(f"⚠ Esperava 401, recebeu {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_complete()
