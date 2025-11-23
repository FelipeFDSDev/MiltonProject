from celery_app import celery_app
from service.agendamento_service import AgendamentoService
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name='tasks.processar_agendamentos')
def processar_agendamentos():
    """
    Tarefa periódica que verifica e processa mensagens agendadas.
    Executada automaticamente pelo Celery Beat.
    """
    try:
        service = AgendamentoService()
        processadas = service.processar_mensagens_pendentes()
        logger.info(f"[CELERY BEAT] {processadas} mensagens processadas.")
        return processadas
    except Exception as e:
        logger.error(f"[CELERY BEAT] Erro ao processar agendamentos: {str(e)}")
        return 0
