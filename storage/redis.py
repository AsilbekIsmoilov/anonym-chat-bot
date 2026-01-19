import redis.asyncio as redis

redis = redis.from_url(
    "redis://localhost:6379/0",
    decode_responses=True
)
