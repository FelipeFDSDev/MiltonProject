# Guia de inicialização local

Este guia corresponde à estrutura atual do projeto. Requisitos detalhados, arquitetura, configuração e limitações estão no [README](../README.md).

## Pré-requisitos

- Python 3.10 ou superior.
- Redis em `localhost:6379` (pode ser executado com Docker).
- Credenciais SMTP para efetuar envio de e-mails. WhatsApp requer alterações descritas no README.

## Instalar dependências

No PowerShell, a partir da raiz do repositório:

```powershell
cd "API Base - Python"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Iniciar os serviços

Inicie o Redis em um terminal:

```powershell
docker run --name redis-milton -p 6379:6379 -d redis
```

Configure as variáveis SMTP descritas no README em `API Base - Python/.env`. Depois, abra terminais separados, ative o ambiente virtual em cada um e execute a partir de `API Base - Python`:

```powershell
python -m uvicorn main:app --reload
```

```powershell
celery -A celery_app worker --loglevel=info -P solo
```

```powershell
celery -A celery_app beat --loglevel=info
```

A API cria as tabelas SQLite ao iniciar. Endpoints de negócio exigem JWT. Registre um usuário por `POST /auth/register`, autentique em `POST /auth/token` e autorize as chamadas com `Authorization: Bearer <token>`. Não use credenciais padrão de exemplos antigos.

- API: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Rotas de agendamento usam `/api/agendamentos/`; veja [AGENDAMENTO.md](../Documentação/AGENDAMENTO.md) para payloads e filtros. Ao terminar, use `Ctrl+C` em cada terminal. Não remova o banco `sql_app.db` se precisar preservar os dados.
