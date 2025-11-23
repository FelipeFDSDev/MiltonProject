from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
import os

# Adiciona o diretório raiz ao path para importar o módulo database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import SQLALCHEMY_DATABASE_URL

def upgrade():
    # Cria uma conexão com o banco de dados
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Verifica se a coluna já existe
        result = db.execute(text("""
            PRAGMA table_info(mensagens_agendadas)
        """))
        
        columns = [row[1] for row in result.fetchall()]
        
        if 'contato_id' not in columns:
            print("Adicionando a coluna 'contato_id' à tabela 'mensagens_agendadas'...")
            
            # Adiciona a nova coluna contato_id
            db.execute(text("""
                ALTER TABLE mensagens_agendadas 
                ADD COLUMN contato_id INTEGER 
                REFERENCES contacts(id)
            
            """))
            db.commit()
            print("Migração concluída com sucesso! A coluna 'contato_id' foi adicionada.")
        else:
            print("A coluna 'contato_id' já existe na tabela 'mensagens_agendadas'.")
            
    except Exception as e:
        db.rollback()
        print(f"Erro durante a migração: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Iniciando migração...")
    upgrade()
    print("Migração finalizada.")
