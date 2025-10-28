"""
Script simples para testar se a API está acessível.
"""

import requests

def testar_api():
    urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://0.0.0.0:8000"
    ]
    
    print("=" * 60)
    print("TESTANDO CONECTIVIDADE COM A API")
    print("=" * 60)
    
    for url in urls:
        print(f"\n🔍 Testando: {url}")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ SUCESSO! Status: {response.status_code}")
                print(f"   📄 Resposta: {response.json()}")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ ERRO: Não foi possível conectar")
        except requests.exceptions.Timeout:
            print(f"   ❌ ERRO: Timeout na conexão")
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
    
    print("\n" + "=" * 60)
    print("RECOMENDAÇÃO:")
    print("Use http://localhost:8000 ou http://127.0.0.1:8000 no navegador")
    print("=" * 60)

if __name__ == "__main__":
    testar_api()
