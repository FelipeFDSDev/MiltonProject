from celery import Celery
from celery.schedules import crontab

# Conexão com Redis (broker + backend)
celery_app = Celery(
    "mensagens",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.timezone = "America/Sao_Paulo"
celery_app.conf.task_serializer = "json"

# Configuração do Celery Beat para executar tarefas periódicas
celery_app.conf.beat_schedule = {
    'processar-mensagens-agendadas': {
        'task': 'service.scheduler.processar_agendamentos',
        'schedule': 60.0,  # Executa a cada 60 segundos (1 minuto)
    },
}
