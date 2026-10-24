# Testar a autenticação

Não há usuário/senha padrão garantidos. Crie sua própria conta pelo endpoint `POST /auth/register` e use as credenciais escolhidas para autenticar.

## Pelo Swagger UI

1. Inicie a API e abra `http://127.0.0.1:8000/docs`.
2. Execute `POST /auth/register` com `username`, `email`, `password` e, opcionalmente, `full_name`.
3. Execute `POST /auth/token`. Esse endpoint recebe formulário (`username` e `password`), não JSON.
4. Copie `access_token` da resposta.
5. Clique em **Authorize** e informe o token. Nas chamadas diretas, use `Authorization: Bearer SEU_TOKEN`.
6. Teste uma rota protegida, como `GET /api/contacts/`.

## Pelo cURL

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario_teste","email":"teste@example.com","password":"senha-forte-123","full_name":"Usuário Teste"}'

curl -X POST "http://127.0.0.1:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario_teste&password=senha-forte-123"

curl -X GET "http://127.0.0.1:8000/api/contacts/" \
  -H "Authorization: Bearer SEU_TOKEN"
```

O token expira em 24 horas. A chave JWT está fixa no código atual; consulte a seção de limitações do README e não use essa configuração em produção.
