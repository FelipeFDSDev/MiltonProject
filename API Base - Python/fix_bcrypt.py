"""
Script para corrigir problemas de compatibilidade entre bcrypt e passlib.
Reinstala as bibliotecas com versões compatíveis.
"""
import subprocess
import sys

def fix_bcrypt():
    """Reinstala bcrypt e passlib com versões compatíveis."""
    print("🔧 Corrigindo compatibilidade entre bcrypt e passlib...")
    print()
    
    # Desinstala versões problemáticas
    print("1. Desinstalando versões antigas...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "bcrypt", "passlib"], 
                      check=False, capture_output=True)
    except Exception as e:
        print(f"   Aviso: {e}")
    
    # Instala versões compatíveis
    print("2. Instalando versões compatíveis...")
    packages = [
        "bcrypt>=4.0.0",
        "passlib[bcrypt]>=1.7.4"
    ]
    
    for package in packages:
        print(f"   Instalando {package}...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  check=True, capture_output=True, text=True)
            print(f"   ✅ {package} instalado com sucesso")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar {package}: {e.stderr}")
            return False
    
    print()
    print("✅ Correção concluída!")
    print()
    print("Agora você pode executar:")
    print("  python check_admin.py")
    
    return True

if __name__ == "__main__":
    fix_bcrypt()

