# 🚀 Guia Rápido - Iniciar Sistema de Agendamento

## Pré-requisitos

- ✅ Python 3.8+
- ✅ Redis instalado e rodando
- ✅ Dependências instaladas (`pip install -r requirements.txt`)

---

## Passo a Passo

### 1️⃣ Iniciar Redis

**Opção A - Docker (Recomendado):**
```bash
docker run -d -p 6379:6379 redis
```

**Opção B - Redis Local:**
```bash
redis-server
```

---

### 2️⃣ Iniciar API FastAPI

Abra um terminal e execute:

```bash
cd "API Base - Python"
uvicorn main:app --reload
```

✅ API estará disponível em: http://localhost:8000
📚 Documentação interativa: http://localhost:8000/docs

---

### 3️⃣ Iniciar Celery Worker

Abra um **NOVO** terminal e execute:

```bash
cd "API Base - Python"
celery -A celery_app worker --loglevel=info -P solo
```

**Nota:** No Windows, use `-P solo` para evitar problemas.

---

### 4️⃣ Iniciar Celery Beat (Agendador)

Abra um **NOVO** terminal e execute:

```bash
cd "API Base - Python"
celery -A celery_app beat --loglevel=info
```

Este processo verifica agendamentos a cada 1 minuto e envia mensagens automaticamente.

---

## ✅ Verificar se Está Funcionando

### Teste 1: API Rodando

Acesse no navegador: http://localhost:8000

Deve retornar:
```json
{
  "status": "ok",
  "service": "Communication and Scheduling API"
}
```

### Teste 2: Criar Agendamento

Execute o script de exemplo:

```bash
python exemplo_agendamento.py
```

Ou use o Swagger UI: http://localhost:8000/docs

---

## 📋 Resumo dos Terminais

Você deve ter **4 terminais abertos**:

| Terminal | Comando | Descrição |
|----------|---------|-----------|
| 1 | `redis-server` ou Docker | Banco de dados para Celery |
| 2 | `uvicorn main:app --reload` | API FastAPI |
| 3 | `celery -A celery_app worker -P solo` | Worker para processar tarefas |
| 4 | `celery -A celery_app beat` | Agendador periódico |

---

## 🧪 Testar o Sistema

### Criar um agendamento para daqui a 2 minutos:

```bash
curl -X POST "http://localhost:8000/agendamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": "email",
    "destinatario": "teste@teste.com",
    "assunto": "Teste",
    "conteudo": "Mensagem de teste!",
    "data_agendamento": "2025-10-24T20:00:00"
  }'
```

### Listar agendamentos ativos:

```bash
curl http://localhost:8000/agendamentos/?status=AGENDADO
```

---

## 🛑 Parar o Sistema

1. Pressione `Ctrl+C` em cada terminal
2. Pare o Redis (se não estiver usando Docker)

---

## ❓ Problemas Comuns

### Redis não conecta
```
Erro: Error connecting to Redis
Solução: Verifique se o Redis está rodando na porta 6379
```

### Celery não processa mensagens
```
Problema: Mensagens não são enviadas
Solução: Verifique se o Celery Beat está rodando
```

### Porta 8000 já em uso
```
Erro: Address already in use
Solução: Use outra porta: uvicorn main:app --port 8001
```

---

## 📚 Documentação Completa

Consulte `Documentação/AGENDAMENTO.md` para detalhes completos sobre:
- Todos os endpoints disponíveis
- Exemplos de uso
- Arquitetura do sistema
- Troubleshooting avançado

---

## 🎯 Próximos Passos

1. Configure suas credenciais de email no arquivo `.env`
2. Configure suas credenciais do Twilio para WhatsApp
3. Teste criar agendamentos para diferentes datas
4. Explore a documentação interativa em `/docs`

**Pronto! Seu sistema de agendamento está funcionando! 🎉**
