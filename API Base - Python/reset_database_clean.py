"""
Script para resetar o banco de dados completamente
Remove todos os contatos inválidos e reseta a estrutura
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, Base, engine, Contact, User, MensagemAgendada, Cliente, HistoricoMensagem

def reset_database():
    """Remove todas as tabelas e recria elas do zero."""
    print("⚠️  AVISO: Este script vai apagar TODOS os dados do banco de dados!")
    print("=" * 80)
    
    confirm = input("Tem certeza que deseja continuar? (sim/nao): ").strip().lower()
    
    if confirm != "sim":
        print("Operação cancelada.")
        return
    
    try:
        # Apaga todas as tabelas
        print("\n🔄 Apagando todas as tabelas...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tabelas removidas com sucesso!")
        
        # Cria todas as tabelas novamente
        print("\n🔄 Recriando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas recriadas com sucesso!")
        
        # Verifica as tabelas criadas
        print("\n📋 Tabelas criadas:")
        print("  - users")
        print("  - contacts")
        print("  - clientes")
        print("  - historico_mensagens")
        print("  - mensagens_agendadas")
        
        print("\n✨ Banco de dados resetado com sucesso!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erro ao resetar o banco: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()
