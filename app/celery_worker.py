import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker",
    include=["app.tasks"],
    broker=os.getenv('CELERY_BROKER'),
    # backend="rpc://"
)

celery_app.conf.update({
    "task_default_queue": "default",
    "task_acks_late": True,
    "task_reject_on_worker_lost": True,
    "task_routes": {
        "app.tasks.*": {"queue": "default"}
    },
    "worker_concurrency": 50
})

SO_ENVIROMENT = os.getenv("SO_ENVIROMENT", "Linux")
# Se quiser rodar em Windows e evitar pool=prefork, pode configurar:
if SO_ENVIROMENT == "Windows":
    print("RODANDO EM AMBIENTE WINDOWS")
    celery_app.conf.worker_pool = "threads"
