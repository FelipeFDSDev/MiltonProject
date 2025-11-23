import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se as variáveis de ambiente necessárias estão definidas
required_env_vars = ['EMAIL_USER', 'EMAIL_PASS']
for var in required_env_vars:
    if not os.getenv(var):
        print(f"AVISO: A variável de ambiente {var} não está definida no arquivo .env")

from celery import Celery
from celery.schedules import crontab

# Configuração do Celery
celery_app = Celery(
    "mensagens",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=['tasks']  # Inclui as tarefas do módulo tasks.py
)

# Configurações gerais
celery_app.conf.update(
    timezone="America/Sao_Paulo",
    task_serializer="json",
    accept_content=['json'],
    result_serializer='json',
    enable_utc=False,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60  # 25 minutos
)

# Configuração do Celery Beat para executar tarefas periódicas
celery_app.conf.beat_schedule = {
    'processar-mensagens-agendadas': {
        'task': 'tasks.processar_agendamentos',  # Caminho atualizado
        'schedule': 60.0,  # Executa a cada 60 segundos (1 minuto)
        'options': {
            'expires': 30.0,  # Expira após 30 segundos se não for executada
        }
    },
}

# Configuração de logs
if os.environ.get('CELERY_DEBUG'):
    celery_app.conf.worker_log_format = (
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    celery_app.conf.worker_task_log_format = (
        '%(asctime)s [%(levelname)s] %(task_name)s[%(task_id)s]: %(message)s'
    )
