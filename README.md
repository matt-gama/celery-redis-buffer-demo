# 📦 Projeto: Celery Redis Buffer Demo

## 🔧 Tecnologias principais
- **FastAPI** – Web server que recebe webhooks do WhatsApp
- **Celery** – Sistema de filas para processamento assíncrono
- **Redis** – Armazenamento temporário (buffer) com TTL por usuário
- **RabbitMQ** – Broker de mensagens (fila)
- **Docker (opcional)** – Para subir Redis/RabbitMQ facilmente

---

## 🎯 Objetivo

Este projeto demonstra uma **arquitetura orientada a eventos** em que eventos recebidos via webhook são:

1. Recebidos pela API FastAPI
2. Processados assíncronamente por um worker Celery
3. Armazenados temporariamente no Redis com TTL
4. Agrupados e processados **apenas após o tempo de espera expirar**
5. Evita múltiplos processamentos desnecessários com controle de debounce

---

## 📚 Caso de uso didático

Imagine que você está construindo um **atendente automatizado via WhatsApp**, que:

- Recebe **várias mensagens** de um mesmo usuário em poucos segundos
- Precisa **esperar o usuário parar de digitar por um tempo (TTL)** antes de processar as mensagens
- Deseja **coletar todas as mensagens enviadas em um curto intervalo de tempo** e só então tomar uma decisão (ex: enviar para IA ou responder)

Este projeto resolve exatamente isso: bufferiza, agrupa e **processa somente após a janela de tempo acabar**, sem duplicidade de tasks nem perda de eventos.

---

## 🩹 Que dor esse projeto resolve?

- Evita **duplicação de tarefas** no Celery
- Controla **reagendamento inteligente** de tasks com TTL reiniciado
- Processa mensagens de forma **mais eficiente, agrupada e inteligente**
- Serve como **base para sistemas reativos ou automações via mensagens**

---

## 🚀 Como rodar o projeto localmente

### 📦 1. Clone o repositório

```bash
git clone https://github.com/matt-gama/celery-redis-buffer-demo.git
cd celery-redis-buffer-demo
```

---

### 🐍 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

---

### 📦 3. Instale as dependências

```bash
pip install -r requirements.txt
```
```bash
pip install -r requirements-dev.txt
```
---

### 🧪 4. Configure seu `.env`

Crie um arquivo `.env` com:

```env
CELERY_BROKER=""
SO_ENVIROMENT="Windows" #or Linux

# Redis config
REDIS_HOST=""
REDIS_PORT=16985
REDIS_USER="default"
REDIS_PASS=""

```

---

### 🧱 5. Suba Redis e RabbitMQ com Docker (opcional)

```bash
docker-compose up -d
```

---

### ⚙️ 6. Rode a API FastAPI

```bash
uvicorn app.main:app --reload
```

---

### 👷 7. Inicie o worker Celery

**Para Windows:**

```bash
celery -A app.celery_worker.celery_app worker --loglevel=info --pool=solo
```

**Para Linux/macOS:**

```bash
celery -A app.celery_worker.celery_app worker --loglevel=info
```

---

### 📤 8. Teste com envio de payload

Você pode usar o script de testes:

```bash
python tests/test_payload_flow.py
```

Ou manualmente:

```bash
curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -d '{"unique_id": "123", "message": "teste"}'
```