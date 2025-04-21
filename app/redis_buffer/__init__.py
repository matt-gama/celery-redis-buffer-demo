import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

# Cria uma instância Redis reutilizável
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    username=os.getenv("REDIS_USER", "default"),
    password=os.getenv("REDIS_PASS", "root"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True  # Retorna strings ao invés de bytes
)
