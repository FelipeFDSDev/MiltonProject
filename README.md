# MiltonProject - API de Agendamento de Mensagens

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Celery](https://img.shields.io/badge/Celery-5.3+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

API REST completa para gerenciamento de contatos e envio de mensagens com sistema de agendamento automático.

## 🚀 Funcionalidades

- ✅ **Gerenciamento de Contatos** - CRUD completo com importação/exportação CSV
- ✅ **Envio Imediato** - Mensagens via Email (SMTP) e WhatsApp (Twilio)
- ✅ **Agendamento Inteligente** - Agende mensagens para data/hora específicas
- ✅ **Processamento Automático** - Celery Beat verifica e envia mensagens agendadas
- ✅ **API RESTful** - Documentação interativa com Swagger UI
- ✅ **Persistência** - Banco de dados SQLite com SQLAlchemy ORM

## 📋 Pré-requisitos

- Python 3.8+
- Redis 6.0+
- Conta Gmail (para envio de emails)
- Conta Twilio (opcional, para WhatsApp)

## ⚡ Início Rápido

### 1. Instalar Dependências

```bash
cd "API Base - Python"
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie o arquivo `.env` na pasta `API Base - Python`:

```env
EMAIL_USER=seu_email@gmail.com
EMAIL_PASS=sua_senha_de_app
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
```

### 3. Iniciar Redis

```bash
docker run -d -p 6379:6379 redis
```

### 4. Executar o Sistema

**Terminal 1 - API:**
```bash
uvicorn main:app --reload
```

**Terminal 2 - Celery Worker:**
```bash
celery -A celery_app worker --loglevel=info -P solo
```

**Terminal 3 - Celery Beat:**
```bash
celery -A celery_app beat --loglevel=info
```

### 5. Testar

```bash
python exemplo_agendamento.py
```

Ou acesse: http://localhost:8000/docs

## 📚 Documentação

- **[Relatório Completo](RELATORIO_COMPLETO.md)** - Guia detalhado de instalação e uso
- **[Sistema de Agendamento](Documentação/AGENDAMENTO.md)** - Documentação técnica completa
- **[Guia Rápido](API%20Base%20-%20Python/INICIAR_SISTEMA.md)** - Passo a passo de inicialização
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🎯 Exemplos de Uso

### Agendar Mensagem para 10 Dias

```bash
curl -X POST "http://localhost:8000/agendamentos/" \
  -H "Content-Type: application/json" \
  -d '{
    "canal": "email",
    "destinatario": "cliente@empresa.com",
    "assunto": "Lembrete Importante",
    "conteudo": "Sua renovação vence em breve!",
    "data_agendamento": "2025-11-03T14:00:00"
  }'
```

### Listar Agendamentos Ativos

```bash
curl http://localhost:8000/agendamentos/?status=AGENDADO
```

### Enviar Mensagem Imediata

```bash
curl -X POST "http://localhost:8000/mensagem/enviar/" \
  -d "canal=email&destinatario=teste@teste.com&conteudo=Olá!&assunto=Teste"
```

## 🏗️ Arquitetura

```
FastAPI (REST API)
    ↓
SQLite (Persistência)
    ↓
Celery Beat (Agendador) → Redis (Broker) → Celery Worker (Processamento)
    ↓
Email (SMTP) / WhatsApp (Twilio)
```

## 📁 Estrutura do Projeto

```
MiltonProject/
├── API Base - Python/
│   ├── routes/              # Endpoints da API
│   ├── service/             # Lógica de negócio
│   ├── main.py             # Aplicação FastAPI
│   ├── models.py           # Modelos de dados
│   ├── celery_app.py       # Configuração Celery
│   └── requirements.txt    # Dependências
├── Documentação/           # Documentação técnica
└── RELATORIO_COMPLETO.md  # Guia completo
```

## 🔧 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/agendamentos/` | Criar agendamento |
| GET | `/agendamentos/` | Listar agendamentos |
| DELETE | `/agendamentos/{id}` | Cancelar agendamento |
| POST | `/mensagem/enviar/` | Enviar mensagem imediata |
| POST | `/contacts/` | Criar contato |
| GET | `/contacts/` | Listar contatos |

## 🐛 Troubleshooting

### Redis não conecta
```bash
redis-cli ping  # Deve retornar PONG
```

### Celery não processa
Verifique se Worker e Beat estão rodando nos terminais separados.

### Erro ao enviar email
Use senha de app do Gmail, não a senha normal. Ative 2FA primeiro.

## 📊 Status do Projeto

- ✅ API REST funcional
- ✅ Sistema de agendamento completo
- ✅ Processamento automático
- ✅ Documentação completa
- ✅ Scripts de teste

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

**MiltonProject Team**

## 🔗 Links Úteis

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Twilio API](https://www.twilio.com/docs)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**
