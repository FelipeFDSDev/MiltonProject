import os
from database import SQLALCHEMY_DATABASE_URL, Base, engine
from sqlalchemy.orm import sessionmaker
from auth import get_password_hash

def reset_database():
    # Fechar todas as conexões existentes
    if os.path.exists("sql_app.db"):
        try:
            os.rename("sql_app.db", "sql_app.db.bak")
            print("Banco de dados antigo renomeado para sql_app.db.bak")
        except Exception as e:
            print(f"Erro ao renomear o banco de dados: {e}")
            print("Tentando forçar a exclusão...")
            try:
                os.remove("sql_app.db")
            except Exception as e:
                print(f"Não foi possível remover o arquivo: {e}")
                return
    
    # Criar novas tabelas
    print("Criando novo banco de dados...")
    Base.metadata.create_all(bind=engine)
    
    # Criar sessão
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Verificar se o usuário admin já existe
        from database import User
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            # Criar usuário admin
            hashed_password = get_password_hash("admin123")
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                full_name="Admin",
                disabled=False
            )
            db.add(admin)
            db.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe.")
            
    except Exception as e:
        print(f"Erro ao criar usuário admin: {e}")
        db.rollback()
    finally:
        db.close()
        print("Banco de dados resetado com sucesso!")
        print("Por favor, reinicie o servidor.")

if __name__ == "__main__":
    reset_database()
