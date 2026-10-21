# MiltonProject — API de agendamento e comunicação

API REST para cadastro de contatos e envio imediato ou agendado de mensagens por e-mail e WhatsApp. O agendamento persistido é verificado periodicamente pelo Celery Beat; as tarefas são processadas pelo Celery Worker usando Redis como broker.

> Projeto acadêmico. Consulte **Limitações conhecidas** antes de usar fora de desenvolvimento: há configurações de segurança e integração que precisam ser ajustadas.

## Objetivo e problema

O sistema busca centralizar contatos e automatizar o envio de lembretes e notificações em horários definidos. Resolve o trabalho manual de acompanhar datas de envio e disparar mensagens individualmente.

## Escopo

Inclui cadastro, consulta, edição, remoção, importação/exportação CSV de contatos; autenticação de usuários por JWT; envio imediato; criação, consulta, alteração e cancelamento de mensagens agendadas; processamento periódico e integração com SMTP e Twilio.

Não inclui interface web, mensagens recorrentes, painel de monitoramento ou garantia de entrega pelo provedor. Clientes existem no modelo de dados, mas não há rotas de gerenciamento identificadas na API atual.

## Requisitos

### Funcionais

- Registrar e autenticar usuários e emitir token de acesso.
- Gerenciar contatos e importar/exportar CSV.
- Enviar mensagem imediata por e-mail ou WhatsApp a um contato.
- Agendar mensagem futura, consultar por status/contato, editar e cancelar enquanto estiver agendada.
- Processar agendamentos vencidos periodicamente e registrar estado do envio.

### Não funcionais

- Expor recursos HTTP em JSON e documentação OpenAPI interativa.
- Persistir dados em SQLite por padrão.
- Proteger rotas de negócio com token Bearer JWT.
- Validar dados de entrada e registrar estados de processamento.
- Manter credenciais de provedores fora do repositório em ambiente de produção (recomendação; veja limitações).

## Tecnologias e arquitetura

- Python; FastAPI e Uvicorn para a API; Pydantic para validação e esquemas.
- SQLAlchemy ORM com SQLite (`sql_app.db`).
- Celery para tarefas em segundo plano e Celery Beat para verificação a cada 60 segundos; Redis como broker/backend.
- SMTP para e-mail e biblioteca Twilio para WhatsApp.
- JWT (`python-jose`) e hashing de senha via Passlib.

```text
Cliente HTTP -> FastAPI / rotas -> serviços -> SQLAlchemy -> SQLite
                         |                         ^
                         +-> Celery Beat -> Redis -> Celery Worker
                                                    -> SMTP / Twilio
```

`API Base - Python/main.py` cria a aplicação e registra rotas; `routes/` contém endpoints; `routers/auth.py` trata autenticação; `service/` concentra envio e regras de agendamento; `database.py` define conexão e modelos ORM; `models.py` define esquemas Pydantic; `celery_app.py` configura Celery; `tasks.py` define a tarefa periódica.

## Pré-requisitos

- Python 3.10 ou superior (dependências atuais usam recursos do Pydantic 2).
- Redis acessível em `localhost:6379`.
- Docker, se for usar o comando abaixo para Redis.
- Conta/servidor SMTP para e-mail. Credenciais Twilio e número habilitado são necessários para WhatsApp, após ajustar a implementação atual.

## Instalação e execução

No PowerShell, a partir da raiz do repositório:

```powershell
cd "API Base - Python"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Inicie o Redis (em outro terminal):

```powershell
docker run --name redis-milton -p 6379:6379 -d redis
```

Configure as variáveis abaixo no ambiente. Depois, inicie cada processo em terminal separado, sempre dentro de `API Base - Python` com o ambiente virtual ativado:

```powershell
python -m uvicorn main:app --reload
```

```powershell
celery -A celery_app worker --loglevel=info -P solo
```

```powershell
celery -A celery_app beat --loglevel=info
```

A API cria tabelas SQLite no startup. Acesse `http://127.0.0.1:8000/docs` (Swagger), `http://127.0.0.1:8000/redoc` ou `http://127.0.0.1:8000/health`.

## Configuração

A API carrega `.env` ao iniciar. Crie `API Base - Python/.env` localmente e não publique segredos:

| Variável | Uso | Padrão |
|---|---|---|
| `EMAIL_USER` | Conta remetente SMTP | obrigatório para e-mail |
| `EMAIL_PASS` | Senha/token SMTP | obrigatório para e-mail |
| `SMTP_HOST` | Servidor SMTP | `smtp.gmail.com` |
| `SMTP_PORT` | Porta SMTP | `587` |
| `SMTP_USE_TLS` | Ativa STARTTLS (`true`/`false`) | `true` |
| `CELERY_DEBUG` | Habilita formato detalhado de logs | não definido |

O Redis está fixado em `redis://localhost:6379/0`. No estado atual, credenciais e remetente WhatsApp Twilio estão fixos como placeholders em `service/whatsapp_channel.py`; variáveis `TWILIO_*` descritas em documentos antigos não são lidas pelo código. O JWT também usa uma chave fixa em `auth.py`; substitua por configuração segura antes de qualquer implantação.

## API

As rotas de contatos, mensagens e agendamentos usam o prefixo `/api` e exigem `Authorization: Bearer <token>`. Autenticação: `POST /auth/register` (JSON de usuário) e `POST /auth/token` (formulário OAuth2 com `username` e `password`). Token válido por 24 horas. Consulte `/docs` para esquemas e respostas completos.

| Método | Endpoint | Uso |
|---|---|---|
| `GET` | `/health` | Verificar disponibilidade |
| `GET` | `/auth/me` | Consultar usuário autenticado |
| `POST`, `GET` | `/api/contacts/` | Criar/listar contatos |
| `GET`, `PUT`, `DELETE` | `/api/contacts/{contact_id}` | Consultar/alterar/remover contato |
| `POST` | `/api/contacts/import/csv` | Importar contatos CSV (`name`, `email` obrigatórios) |
| `GET` | `/api/contacts/export/csv` | Exportar contatos CSV |
| `POST` | `/api/mensagens/enviar/` | Envio imediato (parâmetros `canal`, `contact_id`, `conteudo`, opcional `assunto`) |
| `POST` | `/api/mensagens/agendar/` | Tarefa Celery com atraso em minutos |
| `POST`, `GET` | `/api/agendamentos/` | Criar/listar agendamentos |
| `GET` | `/api/agendamentos/consulta` | Filtrar por `contact_id` e/ou `status` |
| `GET`, `PUT`, `DELETE` | `/api/agendamentos/{id}` | Consultar/alterar/cancelar agendamento |
| `GET` | `/api/agendamentos/ativos/listar` | Listar pendentes |
| `POST` | `/api/agendamentos/processar/manual` | Processar manualmente mensagens vencidas |

Para criar usuário, use `/auth/register`; em seguida, obtenha o token em `/auth/token` e use o botão **Authorize** do Swagger. Agendamentos persistidos usam `contact_id`, `canal` (`email` ou `whatsapp`), `conteudo`, `data_agendamento` ISO 8601 e `assunto` opcional. O contato fornece o destinatário. Datas sem fuso são interpretadas no contexto de `America/Sao_Paulo` no endpoint de criação.

## Banco de dados

SQLite é configurado em `sqlite:///./sql_app.db`, relativo ao diretório de execução (`API Base - Python`). Tabelas ORM: `users`, `contacts`, `clientes`, `mensagens_agendadas` e `historico_mensagens`. As tabelas são criadas automaticamente no startup. Há scripts de migração/manutenção, mas não há fluxo de migração automatizado configurado no startup.

Não apague `sql_app.db` para reiniciar o serviço se precisar manter os dados; faça backup antes de executar scripts `reset_*.py`.

## Testes

A pasta contém scripts `test_*.py` e `teste_*.py`, além de `pytest` nas dependências. Eles não estão organizados numa suíte documentada. Execução exploratória: `python -m pytest` dentro de `API Base - Python`. Testes que enviam e-mail ou acessam serviços externos precisam de configuração e podem gerar efeitos externos.

## Deploy

Não há Dockerfile, manifesto de produção ou pipeline de CI/CD neste repositório. Para uma implantação, execute API, Redis, worker e Beat como processos/serviços supervisionados, configure armazenamento persistente para SQLite e proteja segredos. Antes de publicar, remova logs que imprimem cabeçalhos/tokens e não use a chave JWT fixa ou CORS aberto. WhatsApp requer integração segura com credenciais reais. O projeto, portanto, documenta execução local; deploy de produção ainda exige trabalho.

## Limitações conhecidas

- `auth.py` contém chave JWT fixa e imprime token/dados sensíveis nos logs; o middleware em `main.py` também imprime cabeçalhos das requisições. Não exponha essa configuração publicamente.
- `service/whatsapp_channel.py` tem credenciais Twilio de exemplo fixas e precisa ser configurado antes do uso real.
- CORS permite qualquer origem.
- O `requirements.txt` inclui `psycopg2-binary`, mas a aplicação usa SQLite por padrão.
- O endpoint de cancelamento declara `204 No Content`, apesar de retornar um objeto; clientes devem considerar a implementação atual ao interpretar a resposta.

## Documentação adicional

- [Relatório do projeto](RELATORIO_COMPLETO.md)
- [Guia de inicialização](API%20Base%20-%20Python/INICIAR_SISTEMA.md)
- [Detalhes de agendamento](Documenta%C3%A7%C3%A3o/AGENDAMENTO.md)
- Coleção de requisições: `Documentação/POSTMAN - Base/Microserviço de Agendamento e Comunicação.postman_collection.json`
