import asyncio
import httpx
import random
import string

URL = "http://localhost:8000/webhook"  # ajuste se sua API estiver em outra porta

def random_msg(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def send_payload(unique_id: str, message: str, delay: float = 0):
    if delay:
        await asyncio.sleep(delay)
    payload = {
        "unique_id": unique_id,
        "message": message
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, json=payload)
        print(f"[SEND] ID: {unique_id} | msg: {message} | delay: {delay}s | status: {response.status_code}")

# 01 - Várias solicitações com o mesmo unique_id em tempos diferentes
async def test_same_unique_id_diff_times():
    print("\n--- Teste 01: mesmo unique_id, tempos diferentes ---")
    uid = "1351911172781"
    await send_payload(uid, "msg1")
    await asyncio.sleep(2)
    await send_payload(uid, "msg2")
    await asyncio.sleep(3)
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")
    await send_payload(uid, "msg3")

# 02 - Vários unique_ids diferentes em tempos diferentes
async def test_multiple_unique_ids_diff_times():
    print("\n--- Teste 02: múltiplos unique_ids, tempos diferentes ---")
    tasks = []
    for i in range(5):
        uid = f"user{i}"
        msg = random_msg()
        delay = i * 1.5
        tasks.append(send_payload(uid, msg, delay=delay))
    await asyncio.gather(*tasks)

# 03 - Múltiplas requisições simultâneas com vários unique_ids
async def test_simultaneous_unique_ids():
    print("\n--- Teste 03: requisições simultâneas com múltiplos unique_ids ---")
    tasks = []
    for i in range(10):
        uid = f"simul{i}"
        msg = random_msg()
        tasks.append(send_payload(uid, msg))
    await asyncio.gather(*tasks)

# Execução principal
async def main():
    await test_same_unique_id_diff_times()
    await asyncio.sleep(15)  # aguarda processamento
    await test_multiple_unique_ids_diff_times()
    await asyncio.sleep(15)
    await test_simultaneous_unique_ids()

if __name__ == "__main__":
    asyncio.run(main())
