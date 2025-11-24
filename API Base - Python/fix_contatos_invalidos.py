"""
Script para corrigir dados antigos na tabela de contatos
Adapta os contatos existentes para passar nas novas validações
"""

import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent))

from database import SessionLocal, Contact
from validators import validar_nome, validar_telefone, validar_canal

def corrigir_contatos():
    """Corrige contatos que têm dados inválidos."""
    db = SessionLocal()
    
    try:
        contatos = db.query(Contact).all()
        
        if not contatos:
            print("✅ Nenhum contato para corrigir")
            return
        
        print(f"📋 Encontrados {len(contatos)} contatos")
        print("=" * 80)
        
        corrigidos = 0
        
        for contact in contatos:
            alterado = False
            motivos = []
            
            # Verifica se o nome é válido
            if contact.name and (contact.name.isdigit() or not re.match(r'^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s\'-]+$', contact.name)):
                # Se for só números, gera um nome genérico
                if contact.name.isdigit():
                    contact.name = f"Contato {contact.id}"
                    motivos.append("nome só números → corrigido para genérico")
                    alterado = True
                else:
                    # Se tiver caracteres inválidos, remove eles
                    contact.name = re.sub(r'[^a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s\'-]', '', contact.name).strip()
                    if contact.name:
                        motivos.append("caracteres inválidos removidos")
                        alterado = True
                    else:
                        contact.name = f"Contato {contact.id}"
                        motivos.append("nome vazio → corrigido para genérico")
                        alterado = True
            
            # Verifica se o canal é válido
            if contact.canalPref:
                canal_lower = contact.canalPref.lower()
                if canal_lower not in ["email", "whatsapp"]:
                    contact.canalPref = "email"
                    motivos.append(f"canal '{contact.canalPref}' → alterado para 'email'")
                    alterado = True
                elif canal_lower != contact.canalPref:
                    contact.canalPref = canal_lower
                    alterado = True
            
            # Verifica telefone
            if contact.phone:
                try:
                    # Tenta validar/normalizar o telefone
                    contact.phone = validar_telefone(contact.phone)
                except ValueError as e:
                    contact.phone = None
                    motivos.append(f"telefone inválido → removido ({str(e)})")
                    alterado = True
            
            # Verifica código externo
            if contact.codExterno:
                if not re.match(r'^[a-zA-Z0-9_-]+$', contact.codExterno):
                    contact.codExterno = re.sub(r'[^a-zA-Z0-9_-]', '', contact.codExterno)
                    if contact.codExterno:
                        motivos.append("código externo corrigido")
                        alterado = True
                    else:
                        contact.codExterno = None
                        motivos.append("código externo inválido → removido")
                        alterado = True
            
            if alterado:
                print(f"\n🔧 Contato ID {contact.id} ({contact.email}):")
                for motivo in motivos:
                    print(f"   • {motivo}")
                print(f"   Nome: {contact.name}")
                print(f"   Canal: {contact.canalPref}")
                if contact.phone:
                    print(f"   Telefone: {contact.phone}")
                if contact.codExterno:
                    print(f"   Código: {contact.codExterno}")
                corrigidos += 1
        
        # Salva as alterações
        if corrigidos > 0:
            print("\n" + "=" * 80)
            print(f"💾 Salvando {corrigidos} contatos corrigidos...")
            db.commit()
            print(f"✅ {corrigidos} contatos foram corrigidos e salvos com sucesso!")
        else:
            print("\n✅ Todos os contatos estão válidos!")
        
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao corrigir contatos: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    print("\n🔍 CORRIGINDO DADOS ANTIGOS NA TABELA DE CONTATOS")
    print("=" * 80)
    corrigir_contatos()
