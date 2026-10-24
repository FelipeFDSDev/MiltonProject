# Agendamento de mensagens

Este documento descreve os endpoints da versão atual. A aplicação registra as rotas sob `/api`; elas exigem `Authorization: Bearer <token>`. Consulte o [README](../README.md) para instalação completa, configuração, arquitetura e limitações conhecidas.

## Como funciona

1. Um usuário autenticado cria um agendamento associado a um contato.
2. A API persiste a mensagem em SQLite com status `AGENDADO`.
3. Celery Beat verifica a fila persistida a cada 60 segundos e despacha mensagens vencidas pelo Redis.
4. O Celery Worker tenta enviar pelo canal configurado e o serviço atualiza o status para `ENVIADO` ou `ERRO`.

## Autenticação

Crie uma conta em `POST /auth/register` e obtenha um token em `POST /auth/token` com `username` e `password` como formulário (`application/x-www-form-urlencoded`). Envie o token nas chamadas abaixo como `Authorization: Bearer <token>`. Não há credenciais padrão documentadas.

## Criar agendamento

**POST `/api/agendamentos/`**

O corpo usa `contact_id` (ID de contato existente), `canal` (`email` ou `whatsapp`), `conteudo`, `data_agendamento` em ISO 8601 e `assunto` opcional. O destinatário é obtido do contato (e-mail ou telefone).

```json
{
  "contact_id": 1,
  "canal": "email",
  "assunto": "Lembrete de consulta",
  "conteudo": "Sua consulta está marcada para amanhã.",
  "data_agendamento": "2030-11-03T14:00:00-03:00"
}
```

A data deve ser futura. No endpoint de criação, data sem fuso é interpretada em `America/Sao_Paulo`. Resposta de sucesso: `201 Created`, com o registro e status `AGENDADO`.

## Consultar, alterar e cancelar

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/agendamentos/?status=AGENDADO&skip=0&limit=100` | Lista e filtra por status |
| `GET` | `/api/agendamentos/consulta?contact_id=1&status=AGENDADO` | Filtra por contato e/ou status |
| `GET` | `/api/agendamentos/{id}` | Consulta um registro |
| `PUT` | `/api/agendamentos/{id}` | Atualiza campos de agendamento ainda `AGENDADO` |
| `DELETE` | `/api/agendamentos/{id}` | Cancela um agendamento ainda `AGENDADO` |
| `GET` | `/api/agendamentos/ativos/listar` | Lista agendamentos ativos |
| `POST` | `/api/agendamentos/processar/manual` | Dispara processamento manual dos vencidos |

Os status usados são `AGENDADO`, `ENVIADO`, `CANCELADO` e `ERRO`. A rota DELETE está declarada com status HTTP `204`; não dependa de corpo na resposta.

## Exemplo com cURL

Depois de obter um token e substituir `SEU_TOKEN`, crie uma mensagem associada ao contato de ID 1:

```bash
curl -X POST "http://localhost:8000/api/agendamentos/" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contact_id":1,"canal":"email","assunto":"Teste","conteudo":"Mensagem de teste","data_agendamento":"2030-11-03T14:00:00-03:00"}'
```

## Processamento e dependências

Para processamento automático, mantenha Redis, a API, o Celery Worker e o Celery Beat em execução. O passo a passo com comandos está em [INICIAR_SISTEMA.md](../API%20Base%20-%20Python/INICIAR_SISTEMA.md). A documentação OpenAPI em `/docs` mostra os esquemas e as respostas da versão executada.

E-mail depende das configurações `EMAIL_USER`, `EMAIL_PASS` e, opcionalmente, `SMTP_HOST`, `SMTP_PORT` e `SMTP_USE_TLS`. O canal WhatsApp não está pronto para envio real: credenciais Twilio estão como placeholders no código, não são lidas de variáveis de ambiente.
