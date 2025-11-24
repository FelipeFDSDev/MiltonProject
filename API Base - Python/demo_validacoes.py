#!/usr/bin/env python3
"""
Demonstração prática das validações implementadas
Mostra exemplos de requisições que funcionam e que falham
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║        DEMONSTRAÇÃO DE VALIDAÇÕES - API DE GERENCIAMENTO DE CONTATOS       ║
╚════════════════════════════════════════════════════════════════════════════╝

Este script demonstra todas as validações implementadas na API.

""")

# ============================================================================
print("1️⃣  VALIDAÇÕES DE USUÁRIO")
print("=" * 80)

examples = [
    {
        "titulo": "❌ USERNAME COM APENAS NÚMEROS",
        "dados": {
            "username": "12212312312344525",
            "email": "email22443@gmail.com",
            "full_name": "João Silva",
            "password": "123456"
        },
        "erro": "Nome de usuário não pode conter apenas números",
        "status": 422
    },
    {
        "titulo": "❌ FULL NAME COM APENAS NÚMEROS",
        "dados": {
            "username": "usuario_teste",
            "email": "email22443@gmail.com",
            "full_name": "121212131231233",
            "password": "123456"
        },
        "erro": "Nome completo pode conter apenas letras, espaços, apóstrofos e hífens",
        "status": 422
    },
    {
        "titulo": "❌ FULL NAME COM NÚMEROS E LETRAS MISTURADAS",
        "dados": {
            "username": "usuario_teste",
            "email": "email22443@gmail.com",
            "full_name": "João Silva 123",
            "password": "123456"
        },
        "erro": "Nome completo pode conter apenas letras, espaços, apóstrofos e hífens",
        "status": 422
    },
    {
        "titulo": "❌ SENHA COM MENOS DE 6 CARACTERES",
        "dados": {
            "username": "usuario_teste",
            "email": "email22443@gmail.com",
            "full_name": "João Silva",
            "password": "12345"
        },
        "erro": "String should have at least 6 characters",
        "status": 422
    },
    {
        "titulo": "❌ SENHA VAZIA",
        "dados": {
            "username": "usuario_teste",
            "email": "email22443@gmail.com",
            "full_name": "João Silva",
            "password": ""
        },
        "erro": "String should have at least 6 characters",
        "status": 422
    },
    {
        "titulo": "✅ USUÁRIO VÁLIDO",
        "dados": {
            "username": "usuario_teste_123",
            "email": "usuario@example.com",
            "full_name": "João Silva",
            "password": "SenhaSegura123"
        },
        "erro": None,
        "status": 201
    }
]

for i, example in enumerate(examples, 1):
    print(f"\n{example['titulo']}")
    print("-" * 80)
    print(f"Endpoint: POST /auth/register")
    print(f"Status esperado: HTTP {example['status']}")
    print(f"\nDados enviados:")
    
    import json
    for key, value in example['dados'].items():
        if key == 'password':
            print(f"  \"{key}\": \"{'*' * len(value)}\"")
        else:
            print(f"  \"{key}\": \"{value}\"")
    
    if example['erro']:
        print(f"\n⚠️  Erro esperado:")
        print(f"  \"{example['erro']}\"")
    else:
        print(f"\n✨ Usuário criado com sucesso!")

# ============================================================================
print("\n\n2️⃣  VALIDAÇÕES DE CONTATO")
print("=" * 80)

contact_examples = [
    {
        "titulo": "❌ NOME COM APENAS NÚMEROS",
        "dados": {
            "name": "12212312312344525",
            "email": "email22443@gmail.com",
            "canalPref": "email",
            "phone": "11999998888"
        },
        "erro": "Nome do contato não pode conter apenas números",
        "status": 422
    },
    {
        "titulo": "❌ CANAL INVÁLIDO",
        "dados": {
            "name": "João Silva",
            "email": "joao@example.com",
            "canalPref": "sms",
            "phone": "11999998888"
        },
        "erro": "Canal inválido. Use 'email' ou 'whatsapp'",
        "status": 422
    },
    {
        "titulo": "❌ TELEFONE COM MENOS DE 10 DÍGITOS",
        "dados": {
            "name": "João Silva",
            "email": "joao@example.com",
            "canalPref": "email",
            "phone": "119999"
        },
        "erro": "Telefone deve conter 10 ou 11 dígitos (com DDD)",
        "status": 422
    },
    {
        "titulo": "❌ EMAIL INVÁLIDO",
        "dados": {
            "name": "João Silva",
            "email": "email_invalido",
            "canalPref": "email",
            "phone": "11999998888"
        },
        "erro": "value is not a valid email address",
        "status": 422
    },
    {
        "titulo": "❌ CÓDIGO EXTERNO COM CARACTERES ESPECIAIS",
        "dados": {
            "name": "João Silva",
            "email": "joao@example.com",
            "canalPref": "email",
            "phone": "11999998888",
            "codExterno": "A@#$%"
        },
        "erro": "Código externo deve conter apenas letras, números, hífens ou underscores",
        "status": 422
    },
    {
        "titulo": "✅ CONTATO VÁLIDO (COM TODOS OS CAMPOS)",
        "dados": {
            "name": "João Silva",
            "email": "joao.silva@example.com",
            "canalPref": "email",
            "phone": "11999998888",
            "codExterno": "A0013"
        },
        "erro": None,
        "status": 201
    },
    {
        "titulo": "✅ CONTATO VÁLIDO (MÍNIMO OBRIGATÓRIO)",
        "dados": {
            "name": "Maria Santos",
            "email": "maria.santos@example.com",
            "canalPref": "whatsapp"
        },
        "erro": None,
        "status": 201
    }
]

for i, example in enumerate(contact_examples, 1):
    print(f"\n{example['titulo']}")
    print("-" * 80)
    print(f"Endpoint: POST /contacts/")
    print(f"Status esperado: HTTP {example['status']}")
    print(f"\nDados enviados:")
    
    for key, value in example['dados'].items():
        print(f"  \"{key}\": \"{value}\"")
    
    if example['erro']:
        print(f"\n⚠️  Erro esperado:")
        print(f"  \"{example['erro']}\"")
    else:
        print(f"\n✨ Contato criado com sucesso!")

# ============================================================================
print("\n\n📋 RESUMO DAS VALIDAÇÕES")
print("=" * 80)

validacoes = """
CAMPOS DE USUÁRIO:
├── username: 3-50 caracteres, não pode ser só números
├── email: Formato válido (RFC 5322)
├── full_name: Apenas letras, espaços, apóstrofos, hífens (opcional)
└── password: Mínimo 6 caracteres

CAMPOS DE CONTATO:
├── name: Não pode ser só números
├── email: Formato válido, único no banco
├── phone: 10 ou 11 dígitos (opcional)
├── canalPref: 'email' ou 'whatsapp'
└── codExterno: Letras, números, hífens, underscores (opcional)

CAMPOS DE MENSAGEM:
├── contact_id: Número positivo
├── canal: 'email' ou 'whatsapp'
├── assunto: Máximo 200 caracteres (opcional)
├── conteudo: 1-2000 caracteres
└── data_agendamento: Data futura no formato ISO 8601
"""

print(validacoes)

# ============================================================================
print("\n" + "=" * 80)
print("✅ FIM DA DEMONSTRAÇÃO")
print("=" * 80)
print("""
Para testar na prática:

1. VIA SWAGGER:
   - Acesse: http://localhost:8000/docs
   - Clique em "Try it out" em qualquer endpoint
   - Preencha com dados inválidos e veja os erros

2. VIA CURL (exemplo):
   curl -X POST "http://localhost:8000/auth/register" \\
     -H "Content-Type: application/json" \\
     -d '{
       "username": "usuario123",
       "email": "usuario@example.com",
       "full_name": "João Silva",
       "password": "senha123456"
     }'

3. VIA PYTHON:
   python test_validations.py

""")
