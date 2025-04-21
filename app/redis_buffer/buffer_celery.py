from datetime import timedelta
from app.tasks import process_buffered_data

def set_buffer(key: str, value: str, expire: int = 60):
    redis_client.hset(key, str(int(time.time() * 1000)), value)
    redis_client.expire(key, expire)

    # Agenda task para processar a chave após o TTL
    process_buffered_data.apply_async(args=[key], countdown=expire)