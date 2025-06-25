import redis

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=False)

def get_cached_data(key):
    return redis_client.get(key)

def set_cache(key, value, timeout=60):
    redis_client.setex(key, timeout, value)
