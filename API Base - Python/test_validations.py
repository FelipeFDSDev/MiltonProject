"""
Script de teste para validações de campos
Testa se as validações estão funcionando corretamente
"""
import json
from schemas import UserCreate
from models import ContactBase

def test_user_validations():
    """Testa validações de usuário"""
    print("=" * 60)
    print("TESTANDO VALIDAÇÕES DE USUÁRIO")
    print("=" * 60)
    
    # Teste 1: Username só com números (deve falhar)
    print("\n✗ Teste 1: Username com apenas números")
    try:
        user = UserCreate(
            username="12212312312344525",
            email="email22443@gmail.com",
            full_name="João Silva",
            password="123456"
        )
        print(f"  ❌ FALHA: Aceitou username numérico: {user.username}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 2: Full name só com números (deve falhar)
    print("\n✗ Teste 2: Full name com apenas números")
    try:
        user = UserCreate(
            username="usuario_teste",
            email="email22443@gmail.com",
            full_name="121212131231233",
            password="123456"
        )
        print(f"  ❌ FALHA: Aceitou full_name numérico: {user.full_name}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 3: Full name com números e letras (deve passar)
    print("\n✓ Teste 3: Full name válido com números e letras")
    try:
        user = UserCreate(
            username="usuario_teste",
            email="email22443@gmail.com",
            full_name="João Silva 123",
            password="123456"
        )
        print(f"  ❌ FALHA: Aceitou full_name com números misturados (esperado rejeitar)")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 4: Full name válido (deve passar)
    print("\n✓ Teste 4: Full name válido")
    try:
        user = UserCreate(
            username="usuario_teste",
            email="email22443@gmail.com",
            full_name="João Silva",
            password="123456"
        )
        print(f"  ✓ SUCESSO: Aceitou full_name válido: {user.full_name}")
    except ValueError as e:
        print(f"  ❌ FALHA: Rejeitou nome válido - {str(e)}")
    
    # Teste 5: Senha muito curta (deve falhar)
    print("\n✗ Teste 5: Senha com menos de 6 caracteres")
    try:
        user = UserCreate(
            username="usuario_teste",
            email="email22443@gmail.com",
            full_name="João Silva",
            password="12345"
        )
        print(f"  ❌ FALHA: Aceitou senha curta: {user.password}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 6: Senha vazia (deve falhar)
    print("\n✗ Teste 6: Senha vazia")
    try:
        user = UserCreate(
            username="usuario_teste",
            email="email22443@gmail.com",
            full_name="João Silva",
            password=""
        )
        print(f"  ❌ FALHA: Aceitou senha vazia")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 7: Username válido
    print("\n✓ Teste 7: Username válido (com letras)")
    try:
        user = UserCreate(
            username="usuario_teste_123",
            email="email22443@gmail.com",
            full_name="João Silva",
            password="123456"
        )
        print(f"  ✓ SUCESSO: Aceitou username válido: {user.username}")
    except ValueError as e:
        print(f"  ❌ FALHA: Rejeitou username válido - {str(e)}")


def test_contact_validations():
    """Testa validações de contato"""
    print("\n" + "=" * 60)
    print("TESTANDO VALIDAÇÕES DE CONTATO")
    print("=" * 60)
    
    # Teste 1: Nome só com números (deve falhar)
    print("\n✗ Teste 1: Nome do contato com apenas números")
    try:
        contact = ContactBase(
            name="12212312312344525",
            email="email22443@gmail.com",
            canalPref="email",
            phone="11999998888"
        )
        print(f"  ❌ FALHA: Aceitou name numérico: {contact.name}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 2: Nome válido (deve passar)
    print("\n✓ Teste 2: Nome válido do contato")
    try:
        contact = ContactBase(
            name="João Silva",
            email="joao@example.com",
            canalPref="email",
            phone="11999998888"
        )
        print(f"  ✓ SUCESSO: Aceitou name válido: {contact.name}")
    except ValueError as e:
        print(f"  ❌ FALHA: Rejeitou name válido - {str(e)}")
    
    # Teste 3: Canal inválido (deve falhar)
    print("\n✗ Teste 3: Canal inválido")
    try:
        contact = ContactBase(
            name="João Silva",
            email="joao@example.com",
            canalPref="sms",
            phone="11999998888"
        )
        print(f"  ❌ FALHA: Aceitou canal inválido: {contact.canalPref}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 4: Telefone com formato inválido (deve falhar)
    print("\n✗ Teste 4: Telefone com menos de 10 dígitos")
    try:
        contact = ContactBase(
            name="João Silva",
            email="joao@example.com",
            canalPref="email",
            phone="119999"
        )
        print(f"  ❌ FALHA: Aceitou telefone inválido: {contact.phone}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 5: Email inválido (deve falhar)
    print("\n✗ Teste 5: Email inválido")
    try:
        contact = ContactBase(
            name="João Silva",
            email="email_invalido",
            canalPref="email",
            phone="11999998888"
        )
        print(f"  ❌ FALHA: Aceitou email inválido: {contact.email}")
    except ValueError as e:
        print(f"  ✓ SUCESSO: Rejeitou - {str(e)}")
    
    # Teste 6: Contato completo e válido (deve passar)
    print("\n✓ Teste 6: Contato completo e válido")
    try:
        contact = ContactBase(
            name="João Silva",
            email="joao.silva@example.com",
            canalPref="email",
            phone="11999998888",
            codExterno="A0013"
        )
        print(f"  ✓ SUCESSO: Contato válido criado")
        print(f"    - Nome: {contact.name}")
        print(f"    - Email: {contact.email}")
        print(f"    - Canal: {contact.canalPref}")
        print(f"    - Telefone: {contact.phone}")
        print(f"    - Código Externo: {contact.codExterno}")
    except ValueError as e:
        print(f"  ❌ FALHA: Rejeitou contato válido - {str(e)}")


if __name__ == "__main__":
    try:
        test_user_validations()
        test_contact_validations()
    except Exception as e:
        print(f"\n❌ Erro durante testes: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)
