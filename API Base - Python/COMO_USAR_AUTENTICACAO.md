# Guia de autenticação da API

A autenticação usa JWT Bearer. Não há credencial padrão garantida. Crie uma conta em `POST /auth/register`, autentique em `POST /auth/token` e envie `Authorization: Bearer <access_token>` nas rotas protegidas.

## Pelo Swagger UI

1. Abra `http://127.0.0.1:8000/docs`.
2. Execute `POST /auth/register` com um usuário novo.
3. Execute `POST /auth/token` usando os campos de formulário `username` e `password`.
4. Clique em **Authorize** e informe o valor `access_token` retornado.
5. Teste uma rota protegida, por exemplo `GET /api/contacts/`.

## Pelo cURL

```bash
curl -X POST "http://127.0.0.1:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=SEU_USUARIO&password=SUA_SENHA"

curl -X GET "http://127.0.0.1:8000/api/contacts/" \
  -H "Authorization: Bearer SEU_TOKEN"
```

O token tem validade de 24 horas. Para instruções de instalação e limitações de segurança conhecidas, consulte o [README](../README.md).
