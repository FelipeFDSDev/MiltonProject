from database import SessionLocal, User
from auth import verify_password

def check_admin_password():
    """Verifica se o usuário admin existe e testa a senha padrão."""
    db = SessionLocal()
    try:
        # Buscar o usuário admin
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("❌ Usuário admin não encontrado!")
            print("\nPara criar o usuário admin, execute:")
            print("  python create_admin.py")
            print("\nOu para resetar/criar com nova senha:")
            print("  python reset_admin_password.py")
            return
            
        print("✅ Usuário admin encontrado!")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Conta ativa: {'Sim' if not admin.disabled else 'Não'}")
        print(f"   Criado em: {admin.created_at}")
        print()
        
        # Verificar a senha padrão
        print("Testando senha padrão 'admin123'...")
        is_correct = verify_password("admin123", admin.hashed_password)
        
        if is_correct:
            print("✅ Senha 'admin123' está CORRETA!")
            print("\nVocê pode fazer login com:")
            print("   Username: admin")
            print("   Password: admin123")
        else:
            print("❌ Senha 'admin123' está INCORRETA!")
            print("\nA senha do admin foi alterada ou não é a padrão.")
            print("\nPara resetar a senha, execute:")
            print("  python reset_admin_password.py")
            print("\nOu para definir uma senha específica:")
            print("  python reset_admin_password.py <nova_senha>")
            
    except Exception as e:
        print(f"❌ Erro ao verificar usuário admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_password()
