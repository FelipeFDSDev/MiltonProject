# 🔐 Como Usar a Autenticação - Guia Completo

## 📍 O que é o Swagger UI?

O **Swagger UI** é a página de documentação interativa da sua API. É onde você pode testar todas as rotas diretamente no navegador.

**URL do Swagger UI:** `http://127.0.0.1:8000/docs`

## ⚠️ IMPORTANTE: Diferença entre acessar diretamente vs Swagger UI

### ❌ NÃO FUNCIONA: Acessar diretamente no navegador
```
http://127.0.0.1:8000/api/contacts/
```
**Por quê?** O navegador não envia o header `Authorization` automaticamente.

### ✅ FUNCIONA: Usar o Swagger UI
```
http://127.0.0.1:8000/docs
```
**Por quê?** O Swagger UI permite adicionar o token e envia automaticamente nas requisições.

---

## 🚀 Passo a Passo Completo

### Passo 1: Acesse o Swagger UI

1. Abra o Firefox
2. Digite na barra de endereços: `http://127.0.0.1:8000/docs`
3. Você verá uma página com todas as rotas da API

### Passo 2: Obtenha o Token

1. Na página do Swagger UI, procure pela rota `POST /auth/token`
2. Clique nela para expandir
3. Clique no botão **"Try it out"** (azul)
4. Preencha os campos:
   - **username**: `admin`
   - **password**: `admin123`
   - Deixe `client_id` e `client_secret` em branco
5. Clique no botão **"Execute"** (verde)
6. Você verá uma resposta como:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```
7. **COPIE O `access_token`** (todo o texto longo)

### Passo 3: Adicione o Token no Swagger UI

1. No topo da página do Swagger UI, procure pelo **botão com um cadeado** 🔒
2. Clique no botão **"Authorize"** (ou o ícone de cadeado)
3. Uma janela popup abrirá
4. Você verá uma seção chamada **"bearerAuth"**
5. No campo **"Value"** (ou campo de texto), cole o token que você copiou
   - Cole apenas o token, SEM a palavra "Bearer"
   - Exemplo: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
6. Clique no botão **"Authorize"** dentro da popup
7. A janela fechará automaticamente
8. O botão de cadeado no topo deve ficar **verde** ou mostrar **"Authorized"**

### Passo 4: Teste uma Rota

1. Procure pela rota `GET /api/contacts/`
2. Clique nela para expandir
3. Clique no botão **"Try it out"**
4. Clique no botão **"Execute"**
5. Você deve ver uma resposta com os dados (não mais erro de autenticação)

---

## 🔍 Se o botão "Authorize" não aparecer verde

Se após adicionar o token o botão não ficar verde, tente:

1. **Limpar o cache do navegador:**
   - Firefox: Ctrl+Shift+Delete
   - Selecione "Cache" e limpe

2. **Recarregar a página:**
   - Pressione F5 ou Ctrl+R

3. **Verificar se o token foi colado corretamente:**
   - O token deve ser um texto longo começando com `eyJ`
   - Não deve ter espaços no início ou fim
   - Não deve incluir a palavra "Bearer"

4. **Tentar novamente:**
   - Clique em "Authorize" novamente
   - Cole o token novamente
   - Clique em "Authorize" dentro da popup

---

## 🛠️ Alternativa: Usar Postman ou curl

Se o Swagger UI não funcionar, você pode usar:

### Postman:
1. Crie uma nova requisição
2. Vá em "Authorization"
3. Selecione "Bearer Token"
4. Cole o token
5. Faça a requisição

### curl (linha de comando):
```bash
# Obter token
curl -X POST "http://127.0.0.1:8000/auth/token" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=admin&password=admin123"

# Usar o token (substitua SEU_TOKEN)
curl -X GET "http://127.0.0.1:8000/api/contacts/" ^
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## ✅ Verificação

Se tudo estiver funcionando:
- O botão de cadeado fica verde ou mostra "Authorized"
- As requisições retornam dados (não erro 401)
- No console do servidor aparece: `DEBUG: Token encontrado no header`

