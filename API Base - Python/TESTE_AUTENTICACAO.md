# Como Testar a Autenticação no Swagger UI

## Problema Identificado
O token está sendo gerado corretamente, mas o Swagger UI não está enviando o token nas requisições subsequentes.

## Solução Temporária - Teste Manual

### Passo 1: Obter o Token
1. Acesse: `http://localhost:8000/docs`
2. Clique em "Authorize" (cadeado no topo)
3. Preencha:
   - username: `admin`
   - password: `admin123`
4. Clique em "Authorize"
5. **IMPORTANTE**: Após obter o token, você verá uma resposta como:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```
6. **COPIE O TOKEN** da resposta

### Passo 2: Usar o Token Manualmente
1. Clique em "Authorize" novamente
2. Cole o token completo (sem "Bearer") no campo
3. Clique em "Authorize" novamente
4. Agora teste as rotas

## Solução Alternativa - Usar curl/Postman

```bash
# 1. Obter token
curl -X POST "http://127.0.0.1:8000/auth/token" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=admin&password=admin123"

# 2. Usar o token (substitua SEU_TOKEN)
curl -X GET "http://127.0.0.1:8000/api/contacts/" ^
  -H "Authorization: Bearer SEU_TOKEN"
```

## Verificação no Console
O middleware de debug mostrará:
- `DEBUG: Token encontrado no header: Bearer ...` → Token está sendo enviado ✅
- `DEBUG: Nenhum token encontrado para /api/contacts/` → Token NÃO está sendo enviado ❌

