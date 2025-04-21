from fastapi import FastAPI
from app.tasks import process_event
from app import *

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(payload: dict):
    print(f"[{GREEN}API{RESET}] Webhook recebido: {payload}")
    process_event.apply_async(args=[payload], queue='default')
    return {"message": "Evento recebido e enviado para processamento"}
