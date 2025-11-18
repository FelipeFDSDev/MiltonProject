"""
Script para resetar a senha do usuário admin.
Execute este script para definir uma nova senha para o usuário admin.
"""
from database import SessionLocal, User
from auth import get_password_hash

def reset_admin_password(new_password: str = "admin123"):
    """
    Reseta a senha do usuário admin.
    
    Args:
        new_password: Nova senha para o usuário admin (padrão: "admin123")
    """
    db = SessionLocal()
    try:
        # Buscar o usuário admin
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("⚠️  Usuário admin não encontrado!")
            print("\nCriando novo usuário admin...")
            
            # Criar novo usuário admin
            hashed_password = get_password_hash(new_password)
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                full_name="Admin",
                disabled=False
            )
            db.add(admin)
            db.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("\n" + "="*50)
            print("CREDENCIAIS DE ACESSO:")
            print("="*50)
            print(f"Username: admin")
            print(f"Password: {new_password}")
            print("="*50)
        else:
            # Resetar senha do admin existente
            print(f"🔄 Resetando senha do usuário admin...")
            hashed_password = get_password_hash(new_password)
            admin.hashed_password = hashed_password
            admin.disabled = False
            db.commit()
            print("✅ Senha do usuário admin resetada com sucesso!")
            print("\n" + "="*50)
            print("CREDENCIAIS DE ACESSO:")
            print("="*50)
            print(f"Username: admin")
            print(f"Password: {new_password}")
            print("="*50)
            print("\n⚠️  IMPORTANTE: Anote essas credenciais!")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao resetar senha do admin: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*50)
    print("RESET DE SENHA DO USUÁRIO ADMIN")
    print("="*50)
    
    # Se uma senha foi fornecida como argumento, use ela
    if len(sys.argv) > 1:
        new_password = sys.argv[1]
        print(f"\nDefinindo senha para: {new_password}")
        reset_admin_password(new_password)
    else:
        # Senha padrão
        print("\nUsando senha padrão: admin123")
        print("(Para usar uma senha diferente, execute:)")
        print("  python reset_admin_password.py <nova_senha>")
        print()
        reset_admin_password("admin123")
    
    print("\n✅ Processo concluído!")
    print("\nAgora você pode fazer login na API com essas credenciais.")

