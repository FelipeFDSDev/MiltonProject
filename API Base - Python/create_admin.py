from database import SessionLocal, User
from passlib.context import CryptContext

def create_admin_user():
    db = SessionLocal()
    try:
        # Verificar se o usuário admin já existe
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Usuário admin já existe.")
            return
        
        # Criar hash da senha
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash("admin123")
        
        # Criar usuário admin
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
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar usuário admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
