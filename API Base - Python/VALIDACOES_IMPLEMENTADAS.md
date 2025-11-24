# Validações Implementadas - API de Gerenciamento de Contatos

## 📋 Resumo das Validações

Todas as validações foram implementadas para garantir a integridade dos dados e proporcionar mensagens de erro intuitivas ao usuário. As validações ocorrem no nível Pydantic (antes de chegar ao banco de dados).

---

## 👤 VALIDAÇÕES DE USUÁRIO (schemas.py)

### Campo: `username`
- ✅ **Mínimo**: 3 caracteres
- ✅ **Máximo**: 50 caracteres
- ✅ **Caracteres permitidos**: Letras, números, underscore (_), hífen (-), ponto (.)
- ❌ **Rejeita**: Apenas números (ex: "12212312312344525")
- ❌ **Rejeita**: Caracteres especiais inválidos (ex: @, #, $)

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "Nome de usuário não pode conter apenas números",
      "type": "value_error"
    }
  ]
}
```

### Campo: `email`
- ✅ **Validação**: EmailStr do Pydantic (RFC 5322)
- ✅ **Formato obrigatório**: `usuario@dominio.com`
- ❌ **Rejeita**: Email sem @
- ❌ **Rejeita**: Email sem domínio

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```

### Campo: `full_name` (opcional)
- ✅ **Caracteres permitidos**: Letras (incluindo acentuadas), espaços, apóstrofos, hífens
- ✅ **Suporta**: Nomes em português (João, José, Ação, etc.)
- ❌ **Rejeita**: Apenas números (ex: "121212131231233")
- ❌ **Rejeita**: Mistura de números e letras (ex: "João Silva 123")
- ❌ **Rejeita**: Vazio ou apenas espaços

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "full_name"],
      "msg": "Nome completo pode conter apenas letras, espaços, apóstrofos e hífens",
      "type": "value_error"
    }
  ]
}
```

### Campo: `password`
- ✅ **Mínimo**: 6 caracteres
- ✅ **Máximo**: Sem limite (apenas validação de mínimo)
- ❌ **Rejeita**: Vazio
- ❌ **Rejeita**: Menos de 6 caracteres

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

## 📞 VALIDAÇÕES DE CONTATO (models.py)

### Campo: `name`
- ✅ **Caracteres permitidos**: Letras (incluindo acentuadas), espaços, hífens, apóstrofos
- ✅ **Suporta**: Nomes completos em português
- ❌ **Rejeita**: Apenas números (ex: "12212312312344525")
- ❌ **Rejeita**: Vazio ou apenas espaços

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Nome do contato não pode conter apenas números",
      "type": "value_error"
    }
  ]
}
```

### Campo: `email`
- ✅ **Validação**: EmailStr (RFC 5322)
- ✅ **Obrigatório**
- ✅ **Verificação**: Email único (não pode repetir na base de dados)
- ❌ **Rejeita**: Email inválido

### Campo: `phone` (opcional)
- ✅ **Formato**: 10 ou 11 dígitos (com DDD)
- ✅ **Aceita**: Com ou sem formatação (automaticamente normalizado)
- ❌ **Rejeita**: Menos de 10 dígitos
- ❌ **Rejeita**: Mais de 11 dígitos

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "phone"],
      "msg": "Telefone deve conter 10 ou 11 dígitos (com DDD)",
      "type": "value_error"
    }
  ]
}
```

### Campo: `canalPref`
- ✅ **Valores permitidos**: "email" ou "whatsapp" (case-insensitive)
- ❌ **Rejeita**: Outros valores (ex: "sms", "telegram")

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "canalPref"],
      "msg": "Canal inválido. Use 'email' ou 'whatsapp'",
      "type": "value_error"
    }
  ]
}
```

### Campo: `codExterno` (opcional)
- ✅ **Caracteres permitidos**: Letras, números, hífens, underscores
- ✅ **Exemplo válido**: "A0013", "codigo-123", "codigo_456"
- ❌ **Rejeita**: Caracteres especiais (ex: @, #, $, espaços)

**Exemplo de erro:**
```json
{
  "detail": [
    {
      "loc": ["body", "codExterno"],
      "msg": "Código externo deve conter apenas letras, números, hífens ou underscores",
      "type": "value_error"
    }
  ]
}
```

---

## 📨 VALIDAÇÕES DE MENSAGEM AGENDADA (models.py)

### Campo: `contact_id`
- ✅ **Tipo**: Inteiro positivo
- ❌ **Rejeita**: Zero ou números negativos

### Campo: `canal`
- ✅ **Valores permitidos**: "email" ou "whatsapp"
- ❌ **Rejeita**: Outros canais

### Campo: `assunto` (opcional)
- ✅ **Máximo**: 200 caracteres
- ✅ **Opcional**: Pode ser deixado em branco

### Campo: `conteudo`
- ✅ **Mínimo**: 1 caractere (não vazio)
- ✅ **Máximo**: 2000 caracteres
- ❌ **Rejeita**: Vazio ou apenas espaços

### Campo: `data_agendamento`
- ✅ **Formato**: ISO 8601 (ex: "2025-11-23T14:30:00")
- ✅ **Validação**: Deve ser uma data futura
- ❌ **Rejeita**: Data no passado ou atual

---

## 🧪 Como Testar as Validações

### Via Swagger UI
1. Acesse: `http://localhost:8000/docs`
2. Expanda o endpoint desejado
3. Clique em "Try it out"
4. Preencha os campos com dados inválidos
5. Observe as mensagens de erro

### Via Script Python
```bash
python test_validations.py
```

### Via cURL
```bash
# Teste com username numérico
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "12212312312344525",
    "email": "teste@example.com",
    "full_name": "João Silva",
    "password": "123456"
  }'
```

---

## 📊 Exemplo de Dados Válidos vs Inválidos

### USUÁRIO

❌ **Inválido:**
```json
{
  "username": "12212312312344525",
  "email": "email22443@gmail.com",
  "full_name": "121212131231233",
  "password": "123456"
}
```

✅ **Válido:**
```json
{
  "username": "usuario_teste_123",
  "email": "usuario@example.com",
  "full_name": "João Silva",
  "password": "SenhaSegura123"
}
```

### CONTATO

❌ **Inválido:**
```json
{
  "name": "12212312312344525",
  "email": "invalid-email",
  "canalPref": "sms",
  "phone": "119999"
}
```

✅ **Válido:**
```json
{
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "canalPref": "email",
  "phone": "11999998888",
  "codExterno": "A0013"
}
```

---

## 🔄 Fluxo de Validação

1. **Frontend/Cliente** envia dados no corpo da requisição (JSON)
2. **Pydantic** valida os dados contra o esquema definido
3. **Se há erro** → Retorna erro HTTP 422 (Unprocessable Entity) com detalhes
4. **Se válido** → Continua para validações adicionais no banco de dados
5. **Resposta** → HTTP 201 (Created) com os dados criados ou HTTP 400 com erro específico

---

## 📝 Notas Importantes

- ✅ Todas as mensagens de erro são em **português**
- ✅ Validações ocorrem **antes** de acessar o banco de dados (melhor performance)
- ✅ O Pydantic v2 fornece mensagens estruturadas com `loc`, `msg` e `type`
- ✅ Para campos opcionais, pode-se deixar `null` ou omitir na requisição
- ✅ Email é sempre **validado e único** no sistema
- ✅ Telefone é automaticamente **normalizado** (apenas dígitos)

---

## 🚀 Próximos Passos

Se precisar de validações adicionais, adicione novos `@field_validator` nos esquemas Pydantic.

Exemplo:
```python
@field_validator('campo_novo', mode='after')
@classmethod
def validar_campo_novo(cls, v):
    if not sua_validacao(v):
        raise ValueError("Sua mensagem de erro aqui")
    return v
```
