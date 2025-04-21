import time
import uuid
from . import redis_client

def set_buffer_raw(key: str, value: str, expire: int = 60):
    field = str(int(time.time() * 1000))
    redis_client.hset(key, field, value)
    redis_client.expire(key, expire)
    return True

def register_task_id(key: str, task_id: str, ttl: int = 60):
    redis_key = f"task_id:{key}"
    redis_client.set(redis_key, task_id, ex=ttl)

def get_current_task_id(key: str):
    return redis_client.get(f"task_id:{key}")

def get_all_buffer(key: str):
    return redis_client.hgetall(key)

def delete_buffer(key: str):
    return redis_client.delete(key)

def exists_in_buffer(key: str):
    return redis_client.exists(key)
