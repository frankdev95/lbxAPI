import aioredis
from utils.const import testing, REDIS_URL

redis = None


async def configure_redis_data(key, query_function, expiry_time):
    result = await redis.get(key)

    if result:
        data = result
        storage_source = "redis"
    else:
        data = await query_function
        redis.set(key, data, expire=expiry_time)
        storage_source = "db"

    return {"source": storage_source, "data": data}


async def is_redis_test_mode():
    global redis
    if testing:
        redis = await aioredis.create_redis_pool(REDIS_URL)