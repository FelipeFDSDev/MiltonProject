from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Contact, Base

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def list_all_contacts():
    db = SessionLocal()
    try:
        print("\nLista de todos os contatos:")
        print("-" * 80)
        print(f"{'ID':<5} | {'Nome':<30} | {'Email':<30} | {'Cliente ID':<10}")
        print("-" * 80)
        
        contacts = db.query(Contact).all()
        for contact in contacts:
            print(f"{contact.id:<5} | {contact.name[:30]:<30} | {str(contact.email)[:30]:<30} | {str(contact.cliente_id):<10}")
        
        print("\nContatos com cliente_id = 3:")
        print("-" * 80)
        contacts_cliente_3 = db.query(Contact).filter(Contact.cliente_id == 3).all()
        if not contacts_cliente_3:
            print("Nenhum contato encontrado com cliente_id = 3")
        else:
            for contact in contacts_cliente_3:
                print(f"ID: {contact.id}, Nome: {contact.name}, Email: {contact.email}, Cliente ID: {contact.cliente_id}")
    
    finally:
        db.close()

if __name__ == "__main__":
    list_all_contacts()
