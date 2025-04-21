import ast
import json

from .celery_worker import celery_app
from app.redis_buffer import buffer
from app import *

TIMER_TTL = 12

@celery_app.task(bind=True)
def process_event(self, data: dict):
    print(f"[{YELLOW}Worker{RESET}] Recebido payload")

    unique_id = data.get('unique_id', 'default')
    key = f"user:{unique_id}"

    # Salva no buffer
    buffer.set_buffer_raw(key, str(data), expire=TIMER_TTL+5)

    # Gera novo task_id e agende
    task = process_buffered_data.apply_async(args=[key], countdown=TIMER_TTL)

    # Salva task_id atual como o único válido
    buffer.register_task_id(key, task.id, ttl=TIMER_TTL+5)

    print(f"[{YELLOW}Worker{RESET}] Agendada task {YELLOW}{task.id}{RESET} para chave {key}")

@celery_app.task(bind=True)
def process_buffered_data(self, key):

    task_id = self.request.id
    current_task_id = buffer.get_current_task_id(key)

    if current_task_id != task_id:
        print(f"[{RED}Worker{RESET}] Ignorando task {RED}{task_id}{RESET} — nova task {GREEN}{current_task_id}{RESET} já foi agendada.")
        return

    data = buffer.get_all_buffer(key)
    if data:
        print(f"[{GREEN}PROCESSANDO{RESET}] TASK: {GREEN}{current_task_id}{RESET} Dados expirados da chave {key}")
        print_messages_grouped_by_lead(data)
    else:
        print(f"[{RED}PROCESSANDO{RESET}] Nenhum dado encontrado para {key}")

def print_messages_grouped_by_lead(buffer_data: dict):
    """
    Recebe um dicionário de payloads com timestamp como chave
    e dados como string, e imprime as mensagens agrupadas por unique_id.
    """
    if not buffer_data:
        print("Nenhum dado recebido.")
        return

    if isinstance(buffer_data, str):
        buffer_data = json.loads(buffer_data)

    messages_by_lead = {}

    for timestamp, raw_value in buffer_data.items():
        try:
            payload = ast.literal_eval(raw_value)  # transforma a string em dict
            unique_id = payload.get("unique_id", "desconhecido")
            message = payload.get("message", "")
            messages_by_lead.setdefault(unique_id, []).append(message)
        except Exception as e:
            print(f"Erro ao processar valor {raw_value}: {e}")

    for unique_id, messages in messages_by_lead.items():
        print(f"Mensagens enviadas pelo LEAD: {GREEN}{unique_id}{RESET}")
        for i, msg in enumerate(messages, 1):
            print(f"    {i}. {msg}")