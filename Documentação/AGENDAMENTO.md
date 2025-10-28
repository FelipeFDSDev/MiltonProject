# Sistema de Agendamento de Mensagens

## Visão Geral

O sistema de agendamento permite criar mensagens para serem enviadas em uma data e hora específicas no futuro. Por exemplo, você pode escrever uma mensagem hoje e agendá-la para ser enviada daqui a 10 dias.

## Funcionalidades

- ✅ **Agendar mensagens** para data/hora específicas
- ✅ **Listar agendamentos** com filtros por status
- ✅ **Atualizar agendamentos** pendentes
- ✅ **Cancelar agendamentos** não enviados
- ✅ **Processamento automático** via Celery Beat (a cada 1 minuto)
- ✅ **Suporte para Email e WhatsApp**

## Como Funciona

1. **Você cria um agendamento** via API com data/hora futura
2. **O agendamento é salvo** no banco de dados com status `AGENDADO`
3. **Celery Beat verifica** a cada 1 minuto se há mensagens para enviar
4. **Quando chega o horário**, a mensagem é enviada automaticamente
5. **Status é atualizado** para `ENVIADO` ou `ERRO`

---

## Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Redis

O Redis é necessário para o Celery funcionar. Instale e inicie:

**Windows:**
```bash
# Baixe o Redis do GitHub ou use Docker
docker run -d -p 6379:6379 redis
```

**Linux/Mac:**
```bash
sudo apt-get install redis-server
redis-server
```

### 3. Iniciar a API

```bash
cd "API Base - Python"
uvicorn main:app --reload
```

### 4. Iniciar o Celery Worker

Em um novo terminal:

```bash
cd "API Base - Python"
celery -A celery_app worker --loglevel=info -P solo
```

**Nota:** No Windows, use `-P solo` para evitar problemas com pool de processos.

### 5. Iniciar o Celery Beat (Agendador)

Em outro terminal:

```bash
cd "API Base - Python"
celery -A celery_app beat --loglevel=info
```

---

## Endpoints da API

### 1. Criar Agendamento

**POST** `/agendamentos/`

Cria um novo agendamento de mensagem.

**Body:**
```json
{
  "canal": "email",
  "destinatario": "cliente@teste.com",
  "assunto": "Lembrete de Consulta",
  "conteudo": "Sua consulta está agendada para amanhã às 14h.",
  "data_agendamento": "2025-11-03T14:00:00"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "canal": "email",
  "destinatario": "cliente@teste.com",
  "assunto": "Lembrete de Consulta",
  "conteudo": "Sua consulta está agendada para amanhã às 14h.",
  "data_agendamento": "2025-11-03T14:00:00",
  "status": "AGENDADO",
  "criado_em": "2025-10-24T19:00:00",
  "enviado_em": null,
  "erro_mensagem": null
}
```

---

### 2. Listar Agendamentos

**GET** `/agendamentos/`

Lista todos os agendamentos com filtros opcionais.

**Parâmetros:**
- `status` (opcional): AGENDADO, ENVIADO, CANCELADO, ERRO
- `skip` (opcional): Paginação
- `limit` (opcional): Limite de resultados (padrão: 100)

**Exemplo:**
```
GET /agendamentos/?status=AGENDADO
```

**Resposta (200):**
```json
[
  {
    "id": 1,
    "canal": "email",
    "destinatario": "cliente@teste.com",
    "assunto": "Lembrete",
    "conteudo": "Mensagem de teste",
    "data_agendamento": "2025-11-03T14:00:00",
    "status": "AGENDADO",
    "criado_em": "2025-10-24T19:00:00",
    "enviado_em": null,
    "erro_mensagem": null
  }
]
```

---

### 3. Obter Agendamento Específico

**GET** `/agendamentos/{agendamento_id}`

Retorna detalhes de um agendamento.

**Resposta (200):**
```json
{
  "id": 1,
  "canal": "email",
  "destinatario": "cliente@teste.com",
  "assunto": "Lembrete",
  "conteudo": "Mensagem de teste",
  "data_agendamento": "2025-11-03T14:00:00",
  "status": "AGENDADO",
  "criado_em": "2025-10-24T19:00:00",
  "enviado_em": null,
  "erro_mensagem": null
}
```

---

### 4. Atualizar Agendamento

**PUT** `/agendamentos/{agendamento_id}`

Atualiza um agendamento com status `AGENDADO`.

**Body (todos os campos são opcionais):**
```json
{
  "data_agendamento": "2025-11-05T16:00:00",
  "conteudo": "Conteúdo atualizado"
}
```

**Resposta (200):** Retorna o agendamento atualizado.

---

### 5. Cancelar Agendamento

**DELETE** `/agendamentos/{agendamento_id}`

Cancela um agendamento (altera status para `CANCELADO`).

**Resposta (200):**
```json
{
  "status": "cancelado",
  "id": 1
}
```

---

### 6. Listar Agendamentos Ativos

**GET** `/agendamentos/ativos/listar`

Lista apenas agendamentos com status `AGENDADO`, ordenados por data.

**Resposta (200):** Array de agendamentos ativos.

---

### 7. Processar Agendamentos Manualmente

**POST** `/agendamentos/processar/manual`

Força o processamento imediato de mensagens agendadas (útil para testes).

**Resposta (200):**
```json
{
  "status": "processado",
  "mensagens_processadas": 3
}
```

---

## Exemplos de Uso

### Exemplo 1: Agendar Email para Daqui a 10 Dias

```bash
curl -X POST "http://localhost:8000/agendamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": "email",
    "destinatario": "cliente@empresa.com",
    "assunto": "Renovação de Contrato",
    "conteudo": "Seu contrato vence em breve. Entre em contato para renovar.",
    "data_agendamento": "2025-11-03T09:00:00"
  }'
```

### Exemplo 2: Agendar WhatsApp para Amanhã

```bash
curl -X POST "http://localhost:8000/agendamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": "whatsapp",
    "destinatario": "+5511999998888",
    "conteudo": "Lembrete: Reunião amanhã às 10h!",
    "data_agendamento": "2025-10-25T09:00:00"
  }'
```

### Exemplo 3: Listar Todos os Agendamentos Ativos

```bash
curl -X GET "http://localhost:8000/agendamentos/?status=AGENDADO"
```

### Exemplo 4: Cancelar um Agendamento

```bash
curl -X DELETE "http://localhost:8000/agendamentos/1"
```

---

## Status dos Agendamentos

| Status | Descrição |
|--------|-----------|
| `AGENDADO` | Mensagem aguardando envio |
| `ENVIADO` | Mensagem enviada com sucesso |
| `CANCELADO` | Agendamento cancelado pelo usuário |
| `ERRO` | Falha no envio da mensagem |

---

## Formato de Data/Hora

Use o formato ISO 8601: `YYYY-MM-DDTHH:MM:SS`

**Exemplos:**
- `2025-11-03T14:30:00` (3 de novembro de 2025, 14h30)
- `2025-12-25T08:00:00` (25 de dezembro de 2025, 8h)

**Importante:** As datas são armazenadas em UTC. O Celery está configurado para timezone `America/Sao_Paulo`.

---

## Testando o Sistema

### 1. Criar um Agendamento para Daqui a 2 Minutos

```python
import requests
from datetime import datetime, timedelta

# Data/hora daqui a 2 minutos
data_futura = (datetime.utcnow() + timedelta(minutes=2)).isoformat()

payload = {
    "canal": "email",
    "destinatario": "teste@teste.com",
    "assunto": "Teste de Agendamento",
    "conteudo": "Esta é uma mensagem de teste!",
    "data_agendamento": data_futura
}

response = requests.post("http://localhost:8000/agendamentos/", json=payload)
print(response.json())
```

### 2. Verificar Logs do Celery

Observe os terminais do Celery Worker e Beat para ver o processamento:

```
[CELERY BEAT] 1 mensagens processadas.
[EMAIL] Mensagem enviada para teste@teste.com
```

---

## Troubleshooting

### Redis não está rodando
```
Erro: Error connecting to Redis
Solução: Inicie o Redis (redis-server ou docker)
```

### Celery Beat não processa mensagens
```
Problema: Mensagens não são enviadas automaticamente
Solução: Verifique se o Celery Beat está rodando
```

### Mensagens ficam com status ERRO
```
Problema: Configurações de email/WhatsApp incorretas
Solução: Verifique o arquivo .env e as credenciais
```

---

## Arquitetura

```
┌─────────────┐
│   FastAPI   │ ← API REST
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  SQLite DB  │ ← Armazena agendamentos
└─────────────┘
       ▲
       │
┌──────┴──────┐
│ Celery Beat │ ← Verifica agendamentos a cada 1 min
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Celery Worker│ ← Processa e envia mensagens
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Email/WhatsApp│ ← Canais de envio
└─────────────┘
```

---

## Próximos Passos

- [ ] Adicionar notificações de confirmação
- [ ] Implementar retry automático para erros
- [ ] Dashboard web para visualizar agendamentos
- [ ] Suporte para mensagens recorrentes (diária, semanal)
- [ ] Integração com mais canais (SMS, Telegram)

---

## Suporte

Para dúvidas ou problemas, consulte a documentação do FastAPI e Celery:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Celery Docs](https://docs.celeryq.dev/)
