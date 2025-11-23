from sqlalchemy import create_engine, inspect
from database import Base, engine, SessionLocal, Contact, MensagemAgendada
from sqlalchemy.orm import relationship

def verificar_estrutura_tabela():
    # Cria uma sessão do banco de dados
    db = SessionLocal()
    
    try:
        # Cria um inspetor para verificar o esquema do banco
        inspector = inspect(engine)
        
        # Verifica se a tabela mensagens_agendadas existe
        tabelas = inspector.get_table_names()
        print("Tabelas existentes no banco de dados:")
        for tabela in tabelas:
            print(f"- {tabela}")
        
        if 'mensagens_agendadas' not in tabelas:
            print("\nA tabela 'mensagens_agendadas' não existe no banco de dados.")
            return
        
        # Obtém as colunas da tabela mensagens_agendadas
        colunas = inspector.get_columns('mensagens_agendadas')
        print("\nEstrutura atual da tabela 'mensagens_agendadas':")
        for coluna in colunas:
            print(f"- {coluna['name']} ({coluna['type']})")
        
        # Verifica se a coluna contato_id já existe
        if 'contato_id' not in [col['name'] for col in colunas]:
            print("\nA coluna 'contato_id' não existe na tabela. Adicionando...")
            try:
                with engine.connect() as conn:
                    # Adiciona a coluna contato_id
                    conn.execute('''
                        ALTER TABLE mensagens_agendadas 
                        ADD COLUMN contato_id INTEGER 
                        REFERENCES contacts(id)
                    ''')
                    print("✅ Coluna 'contato_id' adicionada com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao adicionar a coluna 'contato_id': {str(e)}")
        else:
            print("\n✅ A coluna 'contato_id' já existe na tabela.")
        
        # Verifica se a tabela contacts existe
        if 'contacts' not in tabelas:
            print("\n❌ A tabela 'contacts' não existe no banco de dados.")
            return
        
        # Atualiza o modelo Contact se necessário
        if not hasattr(Contact, 'mensagens_agendadas'):
            print("\nAtualizando modelo Contact...")
            try:
                Contact.mensagens_agendadas = relationship(
                    "MensagemAgendada", 
                    back_populates="contato"
                )
                print("✅ Relacionamento 'mensagens_agendadas' adicionado ao modelo Contact")
            except Exception as e:
                print(f"❌ Erro ao atualizar modelo Contact: {str(e)}")
        
        # Atualiza o modelo MensagemAgendada se necessário
        if not hasattr(MensagemAgendada, 'contato'):
            print("\nAtualizando modelo MensagemAgendada...")
            try:
                MensagemAgendada.contato = relationship(
                    "Contact", 
                    back_populates="mensagens_agendadas"
                )
                print("✅ Relacionamento 'contato' adicionado ao modelo MensagemAgendada")
            except Exception as e:
                print(f"❌ Erro ao atualizar modelo MensagemAgendada: {str(e)}")
        
        print("\n✅ Verificação concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Ocorreu um erro: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando verificação da estrutura do banco de dados...\n")
    verificar_estrutura_tabela()