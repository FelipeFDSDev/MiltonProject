from celery_app import celery_app
from service.mensagem_service import MensagemService
from service.agendamento_service import AgendamentoService

@celery_app.task
def agendar_envio(canal, destinatario, conteudo, assunto=None):
    """
    Tarefa Celery que executa o envio no horário agendado (método antigo com countdown).
    """
    service = MensagemService()
    service.enviar_mensagem(canal, destinatario, conteudo, assunto)


@celery_app.task
def processar_agendamentos():
    """
    Tarefa periódica que verifica e processa mensagens agendadas.
    Executada automaticamente pelo Celery Beat.
    """
    service = AgendamentoService()
    processadas = service.processar_mensagens_pendentes()
    print(f"[CELERY BEAT] {processadas} mensagens processadas.")
    return processadas
