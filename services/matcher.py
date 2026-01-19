from storage.redis import redis

async def start_search(user_id: int, location: str):
    queue_key = f"queue:{location}"

    await redis.lpush(queue_key, user_id)

    if await redis.llen(queue_key) >= 2:
        user_a = await redis.rpop(queue_key)
        user_b = await redis.rpop(queue_key)

        if user_a == user_b:
            return None

        await redis.set(f"chat:{user_a}", user_b)
        await redis.set(f"chat:{user_b}", user_a)

        return int(user_a), int(user_b)

    return None


async def stop_chat(user_id: int):
    peer = await redis.get(f"chat:{user_id}")
    if peer:
        await redis.delete(f"chat:{user_id}")
        await redis.delete(f"chat:{peer}")
    return peer
