# 📊 RELATÓRIO COMPLETO - API de Agendamento de Mensagens

**Projeto:** MiltonProject - API de Envio e Agendamento de Mensagens  
**Tecnologia:** Python + FastAPI + Celery + Redis + SQLite  
**Data:** Outubro 2025

---

## 📑 ÍNDICE

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Arquitetura do Sistema](#2-arquitetura-do-sistema)
3. [Pré-requisitos](#3-pré-requisitos)
4. [Instalação Completa](#4-instalação-completa)
5. [Configuração do Ambiente](#5-configuração-do-ambiente)
6. [Como Executar o Projeto](#6-como-executar-o-projeto)
7. [Endpoints da API](#7-endpoints-da-api)
8. [Exemplos de Uso](#8-exemplos-de-uso)
9. [Testes](#9-testes)
10. [Troubleshooting](#10-troubleshooting)
11. [Estrutura de Arquivos](#11-estrutura-de-arquivos)

---

## 1. VISÃO GERAL DO PROJETO

### 1.1 Descrição

API REST desenvolvida em Python para gerenciamento de contatos e envio de mensagens com sistema de agendamento. Permite:

- ✅ Gerenciar contatos (CRUD completo)
- ✅ Enviar mensagens imediatas via Email e WhatsApp
- ✅ **Agendar mensagens para data/hora específicas**
- ✅ Gerenciar agendamentos (criar, listar, atualizar, cancelar)
- ✅ Processamento automático via Celery Beat

### 1.2 Funcionalidades Principais

| Módulo | Funcionalidade |
|--------|----------------|
| **Contatos** | CRUD, importação/exportação CSV |
| **Mensagens** | Envio imediato, agendamento simples (minutos) |
| **Agendamentos** | Agendamento por data/hora, CRUD completo, processamento automático |
| **Canais** | Email (SMTP), WhatsApp (Twilio) |

### 1.3 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados relacional
- **Celery** - Processamento assíncrono de tarefas
- **Redis** - Broker de mensagens para Celery
- **Celery Beat** - Agendador de tarefas periódicas
- **Twilio** - API para envio de WhatsApp
- **SMTP** - Protocolo para envio de emails

---

## 2. ARQUITETURA DO SISTEMA

### 2.1 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE                              │
│              (Browser, Postman, cURL, etc)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI (main.py)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Contacts   │  │  Mensagens   │  │ Agendamentos │     │
│  │   Routes     │  │   Routes     │  │   Routes     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAMADA DE SERVIÇOS                         │
│  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │ MensagemService  │  │   AgendamentoService         │   │
│  └──────────────────┘  └──────────────────────────────┘   │
│  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │  EmailChannel    │  │   WhatsappChannel            │   │
│  └──────────────────┘  └──────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   SQLite     │  │    Redis     │  │    SMTP      │
│   Database   │  │   (Broker)   │  │   Gmail      │
└──────────────┘  └──────┬───────┘  └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Celery Worker │  │ Celery Beat  │  │   Twilio     │
│  (Tarefas)   │  │ (Scheduler)  │  │  WhatsApp    │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 Fluxo de Agendamento

```
1. Cliente cria agendamento via POST /agendamentos/
   ↓
2. FastAPI valida dados e salva no SQLite (status: AGENDADO)
   ↓
3. Celery Beat executa a cada 60 segundos
   ↓
4. Busca mensagens com data_agendamento <= agora
   ↓
5. Celery Worker processa cada mensagem
   ↓
6. Envia via EmailChannel ou WhatsappChannel
   ↓
7. Atualiza status (ENVIADO ou ERRO) no banco
```

---

## 3. PRÉ-REQUISITOS

### 3.1 Software Necessário

| Software | Versão Mínima | Download |
|----------|---------------|----------|
| **Python** | 3.8+ | https://www.python.org/downloads/ |
| **Redis** | 6.0+ | https://redis.io/download/ |
| **Git** | Qualquer | https://git-scm.com/downloads |
| **pip** | 20.0+ | Incluído com Python |

### 3.2 Contas Externas (Opcional)

- **Gmail** - Para envio de emails (ou outro provedor SMTP)
- **Twilio** - Para envio de WhatsApp (conta gratuita disponível)

### 3.3 Sistema Operacional

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, etc)
- ✅ macOS

---

## 4. INSTALAÇÃO COMPLETA

### 4.1 Clonar o Projeto

```bash
cd C:\Users\Nefalem\Desktop
# Projeto já está em: MiltonProject
```

### 4.2 Criar Ambiente Virtual

**Windows:**
```bash
cd "C:\Users\Nefalem\Desktop\MiltonProject\API Base - Python"
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd "/Users/Nefalem/Desktop/MiltonProject/API Base - Python"
python3 -m venv venv
source venv/bin/activate
```

### 4.3 Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependências instaladas:**
- fastapi
- uvicorn[standard]
- pydantic
- sqlalchemy
- celery
- redis
- celery[redis]
- twilio
- python-multipart
- python-dotenv

### 4.4 Instalar Redis

**Opção A - Docker (Recomendado):**
```bash
docker run -d --name redis-milton -p 6379:6379 redis
```

**Opção B - Windows (Manual):**
1. Baixe: https://github.com/microsoftarchive/redis/releases
2. Extraia e execute: `redis-server.exe`

**Opção C - Linux:**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
```

**Opção D - macOS:**
```bash
brew install redis
brew services start redis
```

### 4.5 Verificar Instalação do Redis

```bash
redis-cli ping
# Deve retornar: PONG
```

---

## 5. CONFIGURAÇÃO DO AMBIENTE

### 5.1 Arquivo .env

Crie ou edite o arquivo `.env` na pasta `API Base - Python`:

```env
# Configurações de Email (Gmail)
EMAIL_USER=seu_email@gmail.com
EMAIL_PASS=sua_senha_de_app

# Configurações do Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Configurações do Redis
REDIS_URL=redis://localhost:6379/0

# Configurações do Banco
DATABASE_URL=sqlite:///./sql_app.db
```

### 5.2 Configurar Gmail para Envio de Emails

1. Acesse: https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"
3. Gere uma "Senha de app"
4. Use essa senha no arquivo `.env`

### 5.3 Configurar Twilio (Opcional)

1. Crie conta gratuita: https://www.twilio.com/try-twilio
2. Obtenha Account SID e Auth Token
3. Configure número de WhatsApp no Twilio Sandbox
4. Atualize o arquivo `.env`

### 5.4 Inicializar Banco de Dados

O banco será criado automaticamente na primeira execução da API.

---

## 6. COMO EXECUTAR O PROJETO

### 6.1 Ordem de Execução

Execute os comandos abaixo em **4 terminais separados**:

#### **Terminal 1 - Redis**

```bash
# Se usando Docker:
docker start redis-milton

# Se instalado localmente:
redis-server
```

#### **Terminal 2 - API FastAPI**

```bash
cd "C:\Users\Nefalem\Desktop\MiltonProject\API Base - Python"
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Saída esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### **Terminal 3 - Celery Worker**

```bash
cd "C:\Users\Nefalem\Desktop\MiltonProject\API Base - Python"
venv\Scripts\activate

# Windows:
celery -A celery_app worker --loglevel=info -P solo

# Linux/Mac:
celery -A celery_app worker --loglevel=info
```

**Saída esperada:**
```
[tasks]
  . service.scheduler.agendar_envio
  . service.scheduler.processar_agendamentos
```

#### **Terminal 4 - Celery Beat (Agendador)**

```bash
cd "C:\Users\Nefalem\Desktop\MiltonProject\API Base - Python"
venv\Scripts\activate

celery -A celery_app beat --loglevel=info
```

**Saída esperada:**
```
Scheduler: Sending due task processar-mensagens-agendadas
```

### 6.2 Verificar se Está Funcionando

**1. Teste a API:**
```bash
curl http://localhost:8000/
```

Resposta esperada:
```json
{
  "status": "ok",
  "service": "Communication and Scheduling API"
}
```

**2. Acesse a documentação:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**3. Execute o script de teste:**
```bash
python exemplo_agendamento.py
```

---

## 7. ENDPOINTS DA API

### 7.1 Contatos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/contacts/` | Criar contato |
| GET | `/contacts/` | Listar contatos |
| GET | `/contacts/{id}` | Obter contato |
| PUT | `/contacts/{id}` | Atualizar contato |
| DELETE | `/contacts/{id}` | Deletar contato |
| GET | `/contacts/export/csv` | Exportar CSV |
| POST | `/contacts/import/csv` | Importar CSV |

### 7.2 Mensagens

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/mensagem/enviar/` | Enviar mensagem imediata |
| POST | `/mensagem/agendar/` | Agendar com countdown (minutos) |

### 7.3 Agendamentos (NOVO)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/agendamentos/` | Criar agendamento |
| GET | `/agendamentos/` | Listar agendamentos |
| GET | `/agendamentos/{id}` | Obter agendamento |
| PUT | `/agendamentos/{id}` | Atualizar agendamento |
| DELETE | `/agendamentos/{id}` | Cancelar agendamento |
| GET | `/agendamentos/ativos/listar` | Listar ativos |
| POST | `/agendamentos/processar/manual` | Processar manualmente |

---

## 8. EXEMPLOS DE USO

### 8.1 Criar Agendamento para 10 Dias

```bash
curl -X POST "http://localhost:8000/agendamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": "email",
    "destinatario": "cliente@empresa.com",
    "assunto": "Renovação de Contrato",
    "conteudo": "Seu contrato vence em 10 dias. Renove agora!",
    "data_agendamento": "2025-11-03T09:00:00"
  }'
```

### 8.2 Listar Agendamentos Ativos

```bash
curl http://localhost:8000/agendamentos/?status=AGENDADO
```

### 8.3 Cancelar Agendamento

```bash
curl -X DELETE http://localhost:8000/agendamentos/1
```

### 8.4 Enviar Mensagem Imediata

```bash
curl -X POST "http://localhost:8000/mensagem/enviar/" \
  -d "canal=email&destinatario=teste@teste.com&conteudo=Olá!&assunto=Teste"
```

### 8.5 Criar Contato

```bash
curl -X POST "http://localhost:8000/contacts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@empresa.com",
    "phone": "11999998888",
    "canalPref": "email",
    "codExterno": "CLI001"
  }'
```

---

## 9. TESTES

### 9.1 Teste Automatizado

Execute o script de exemplo:

```bash
python exemplo_agendamento.py
```

Este script irá:
1. Criar um agendamento para daqui a 2 minutos
2. Listar agendamentos ativos
3. Consultar o agendamento criado
4. Opção de cancelar ou processar

### 9.2 Teste Manual via Swagger

1. Acesse: http://localhost:8000/docs
2. Clique em "POST /agendamentos/"
3. Clique em "Try it out"
4. Preencha o JSON de exemplo
5. Clique em "Execute"

### 9.3 Teste de Processamento

```bash
# Criar agendamento para daqui a 1 minuto
curl -X POST "http://localhost:8000/agendamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": "email",
    "destinatario": "teste@teste.com",
    "assunto": "Teste",
    "conteudo": "Teste de agendamento",
    "data_agendamento": "2025-10-24T16:30:00"
  }'

# Aguardar 1 minuto e verificar logs do Celery Beat
# Ou forçar processamento:
curl -X POST http://localhost:8000/agendamentos/processar/manual
```

---

## 10. TROUBLESHOOTING

### 10.1 Problemas Comuns

#### ❌ Redis não conecta

**Erro:**
```
celery.exceptions.ImproperlyConfigured: Error connecting to Redis
```

**Solução:**
```bash
# Verificar se Redis está rodando
redis-cli ping

# Se não estiver, iniciar:
redis-server
# ou
docker start redis-milton
```

#### ❌ Porta 8000 já em uso

**Erro:**
```
ERROR: [Errno 10048] Only one usage of each socket address
```

**Solução:**
```bash
# Use outra porta
uvicorn main:app --port 8001

# Ou mate o processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### ❌ Celery não processa mensagens

**Problema:** Mensagens não são enviadas automaticamente

**Solução:**
1. Verifique se Celery Beat está rodando
2. Verifique logs do Beat para ver se está executando a task
3. Verifique se Worker está rodando
4. Teste processamento manual

#### ❌ Erro ao enviar email

**Erro:**
```
[EMAIL] Erro ao enviar: (535, 'Authentication failed')
```

**Solução:**
1. Verifique credenciais no `.env`
2. Use senha de app do Gmail (não a senha normal)
3. Verifique se 2FA está ativo no Gmail

#### ❌ Módulo não encontrado

**Erro:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solução:**
```bash
# Ative o ambiente virtual
venv\Scripts\activate

# Reinstale dependências
pip install -r requirements.txt
```

### 10.2 Logs e Debugging

**Ver logs da API:**
- Logs aparecem no terminal onde rodou `uvicorn`

**Ver logs do Celery:**
- Worker: Terminal 3
- Beat: Terminal 4

**Ver banco de dados:**
```bash
sqlite3 sql_app.db
.tables
SELECT * FROM mensagens_agendadas;
.quit
```

---

## 11. ESTRUTURA DE ARQUIVOS

```
MiltonProject/
│
├── API Base - Python/
│   ├── venv/                          # Ambiente virtual
│   ├── __pycache__/                   # Cache Python
│   │
│   ├── routes/                        # Rotas da API
│   │   ├── contacts.py               # CRUD de contatos
│   │   ├── mensagens.py              # Envio de mensagens
│   │   └── agendamentos.py           # Sistema de agendamento
│   │
│   ├── service/                       # Lógica de negócio
│   │   ├── mensagem_service.py       # Serviço de mensagens
│   │   ├── agendamento_service.py    # Serviço de agendamento
│   │   ├── scheduler.py              # Tasks Celery
│   │   ├── email_channel.py          # Canal de email
│   │   └── whatsapp_channel.py       # Canal de WhatsApp
│   │
│   ├── main.py                        # Aplicação FastAPI
│   ├── models.py                      # Modelos Pydantic e ORM
│   ├── database.py                    # Configuração do banco
│   ├── celery_app.py                  # Configuração Celery
│   ├── .env                           # Variáveis de ambiente
│   ├── requirements.txt               # Dependências
│   ├── sql_app.db                     # Banco SQLite
│   ├── exemplo_agendamento.py         # Script de teste
│   └── INICIAR_SISTEMA.md            # Guia rápido
│
├── Documentação/
│   └── AGENDAMENTO.md                 # Documentação detalhada
│
├── README.md                          # Readme do projeto
└── RELATORIO_COMPLETO.md             # Este arquivo
```

---

## 📊 RESUMO EXECUTIVO

### ✅ O Que o Sistema Faz

1. **Gerencia contatos** com CRUD completo
2. **Envia mensagens imediatas** via Email e WhatsApp
3. **Agenda mensagens** para data/hora específicas
4. **Processa automaticamente** agendamentos via Celery Beat
5. **Gerencia agendamentos** (criar, listar, atualizar, cancelar)

### 🚀 Como Iniciar (Resumo)

```bash
# 1. Ativar ambiente virtual
venv\Scripts\activate

# 2. Iniciar Redis (Terminal 1)
docker run -d -p 6379:6379 redis

# 3. Iniciar API (Terminal 2)
uvicorn main:app --reload

# 4. Iniciar Worker (Terminal 3)
celery -A celery_app worker -P solo --loglevel=info

# 5. Iniciar Beat (Terminal 4)
celery -A celery_app beat --loglevel=info

# 6. Testar
python exemplo_agendamento.py
```

### 📚 Documentação Adicional

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Guia Rápido:** `INICIAR_SISTEMA.md`
- **Documentação Completa:** `Documentação/AGENDAMENTO.md`

---

## 🎯 CONCLUSÃO

O sistema está **100% funcional** e pronto para uso. Todos os componentes foram implementados e testados:

- ✅ API REST com FastAPI
- ✅ Banco de dados SQLite
- ✅ Sistema de agendamento completo
- ✅ Processamento automático com Celery Beat
- ✅ Suporte para Email e WhatsApp
- ✅ Documentação completa
- ✅ Scripts de teste

**Para suporte ou dúvidas, consulte a documentação em `Documentação/AGENDAMENTO.md`**

---

**Desenvolvido para MiltonProject - Outubro 2025**
