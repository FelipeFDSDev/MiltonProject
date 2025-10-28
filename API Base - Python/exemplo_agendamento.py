"""
Script de exemplo para testar o sistema de agendamento de mensagens.
Execute este script após iniciar a API, Celery Worker e Celery Beat.
"""

import requests
from datetime import datetime, timedelta

# URL base da API
BASE_URL = "http://localhost:8000"

def criar_agendamento_teste():
    """
    Cria um agendamento de teste para daqui a 2 minutos.
    """
    print("=" * 60)
    print("CRIANDO AGENDAMENTO DE TESTE")
    print("=" * 60)
    
    # Calcula data/hora daqui a 2 minutos
    data_futura = datetime.utcnow() + timedelta(minutes=2)
    data_futura_str = data_futura.strftime("%Y-%m-%dT%H:%M:%S")
    
    payload = {
        "canal": "email",
        "destinatario": "felipefrs2007@gmail.com",
        "assunto": "Teste de Agendamento",
        "conteudo": "Esta mensagem foi agendada para ser enviada automaticamente!",
        "data_agendamento": data_futura_str
    }
    
    print(f"\n📅 Agendando mensagem para: {data_futura_str}")
    print(f"📧 Destinatário: {payload['destinatario']}")
    print(f"📝 Assunto: {payload['assunto']}")
    
    try:
        response = requests.post(f"{BASE_URL}/agendamentos/", json=payload)
        response.raise_for_status()
        
        resultado = response.json()
        print(f"\n✅ Agendamento criado com sucesso!")
        print(f"   ID: {resultado['id']}")
        print(f"   Status: {resultado['status']}")
        print(f"   Será enviado em: {resultado['data_agendamento']}")
        
        return resultado['id']
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro ao criar agendamento: {e}")
        return None


def listar_agendamentos_ativos():
    """
    Lista todos os agendamentos ativos.
    """
    print("\n" + "=" * 60)
    print("LISTANDO AGENDAMENTOS ATIVOS")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/agendamentos/?status=AGENDADO")
        response.raise_for_status()
        
        agendamentos = response.json()
        
        if not agendamentos:
            print("\n📭 Nenhum agendamento ativo encontrado.")
        else:
            print(f"\n📬 {len(agendamentos)} agendamento(s) ativo(s):\n")
            for ag in agendamentos:
                print(f"   ID: {ag['id']}")
                print(f"   Canal: {ag['canal']}")
                print(f"   Destinatário: {ag['destinatario']}")
                print(f"   Agendado para: {ag['data_agendamento']}")
                print(f"   Status: {ag['status']}")
                print("-" * 60)
        
        return agendamentos
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro ao listar agendamentos: {e}")
        return []


def obter_agendamento(agendamento_id):
    """
    Obtém detalhes de um agendamento específico.
    """
    print("\n" + "=" * 60)
    print(f"CONSULTANDO AGENDAMENTO ID: {agendamento_id}")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/agendamentos/{agendamento_id}")
        response.raise_for_status()
        
        ag = response.json()
        
        print(f"\n📋 Detalhes do Agendamento:")
        print(f"   ID: {ag['id']}")
        print(f"   Canal: {ag['canal']}")
        print(f"   Destinatário: {ag['destinatario']}")
        print(f"   Assunto: {ag['assunto']}")
        print(f"   Conteúdo: {ag['conteudo']}")
        print(f"   Data Agendamento: {ag['data_agendamento']}")
        print(f"   Status: {ag['status']}")
        print(f"   Criado em: {ag['criado_em']}")
        print(f"   Enviado em: {ag['enviado_em']}")
        print(f"   Erro: {ag['erro_mensagem']}")
        
        return ag
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro ao consultar agendamento: {e}")
        return None


def cancelar_agendamento(agendamento_id):
    """
    Cancela um agendamento.
    """
    print("\n" + "=" * 60)
    print(f"CANCELANDO AGENDAMENTO ID: {agendamento_id}")
    print("=" * 60)
    
    try:
        response = requests.delete(f"{BASE_URL}/agendamentos/{agendamento_id}")
        response.raise_for_status()
        
        resultado = response.json()
        print(f"\n✅ Agendamento {resultado['id']} cancelado com sucesso!")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro ao cancelar agendamento: {e}")
        return False


def processar_manualmente():
    """
    Força o processamento manual de agendamentos.
    """
    print("\n" + "=" * 60)
    print("PROCESSANDO AGENDAMENTOS MANUALMENTE")
    print("=" * 60)
    
    try:
        response = requests.post(f"{BASE_URL}/agendamentos/processar/manual")
        response.raise_for_status()
        
        resultado = response.json()
        print(f"\n✅ Processamento concluído!")
        print(f"   Mensagens processadas: {resultado['mensagens_processadas']}")
        
        return resultado
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro ao processar agendamentos: {e}")
        return None


def exemplo_completo():
    """
    Executa um exemplo completo de uso do sistema.
    """
    print("\n" + "=" * 60)
    print("🚀 EXEMPLO COMPLETO DE USO DO SISTEMA DE AGENDAMENTO")
    print("=" * 60)
    
    # 1. Criar agendamento
    agendamento_id = criar_agendamento_teste()
    
    if not agendamento_id:
        print("\n❌ Não foi possível criar o agendamento. Verifique se a API está rodando.")
        return
    
    # 2. Listar agendamentos ativos
    input("\n⏸️  Pressione ENTER para listar agendamentos ativos...")
    listar_agendamentos_ativos()
    
    # 3. Consultar o agendamento criado
    input("\n⏸️  Pressione ENTER para consultar o agendamento criado...")
    obter_agendamento(agendamento_id)
    
    # 4. Opção de cancelar
    print("\n" + "=" * 60)
    opcao = input("\n❓ Deseja cancelar este agendamento? (s/n): ").lower()
    
    if opcao == 's':
        cancelar_agendamento(agendamento_id)
        input("\n⏸️  Pressione ENTER para verificar o status...")
        obter_agendamento(agendamento_id)
    else:
        print("\n⏳ Agendamento mantido. Aguarde o Celery Beat processar (a cada 1 minuto).")
        print("   Ou force o processamento manual...")
        
        opcao_processar = input("\n❓ Deseja processar manualmente agora? (s/n): ").lower()
        if opcao_processar == 's':
            processar_manualmente()
            input("\n⏸️  Pressione ENTER para verificar o status...")
            obter_agendamento(agendamento_id)
    
    print("\n" + "=" * 60)
    print("✅ EXEMPLO CONCLUÍDO!")
    print("=" * 60)


if __name__ == "__main__":
    # Verifica se a API está acessível
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        print("✅ API está rodando!")
    except:
        print("❌ ERRO: API não está acessível em http://localhost:8000")
        print("   Certifique-se de que a API está rodando antes de executar este script.")
        exit(1)
    
    # Executa o exemplo completo
    exemplo_completo()
