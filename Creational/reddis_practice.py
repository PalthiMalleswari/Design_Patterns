#  About Reddis
"""
Redis = Remote Dictionary Server.

1.In-memory (very fast)
2.Key-value database
3.Supports TTL expiration
4.Persists data if needed
5.Used widely for caching, sessions, queues, pub/sub

Redis is 10–100× faster than a traditional database because it runs in RAM, not disk.
"""

#  Why Reddis

"""
1.Super fast (sub-millisecond fetching)
2.Supports expiration (TTL)
3.Can store any serialized object (JSON, Pickle)
4.Shared across:
    .multiple Python scripts
    .multiple servers
    .Celery workers
    .microservices
"""


import redis
import time
import json

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

print(redis_client.ping())


redis_client.set("session_token", "xyz123", ex=3)
print(redis_client.get("session_token"))
time.sleep(3)
print(redis_client.get("session_token"))# session expired so returned None


class RedisCache:

    def __init__(self,host='localhost',port=6379,db=0):

        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
    
    def set(self,key,value,ttl=None):
        
        value_json = json.dumps(value)
        self.client.set(key,value_json,ex=ttl)

    def get(self,key):

        data = self.client.get(key)
        return json.loads(data) if data else None
    
    def delete(self,key):

        self.client.delete(key)

    def exists(self,key):

        return self.client.exists(key)
     
#usage

cache = RedisCache()

def get_user_from_api(user_id):

    time.sleep(2)  # Simulate slow API

    return {"id": user_id, "score": 100}

def get_user(user_id):

    start = time.perf_counter()

    key = f"user:{user_id}"
    cached = cache.get(key)

    if cached:
        print(f"Cache Hit! Took {(time.perf_counter() - start)*1000:.3f} ms")
        return cached
    
    print("Cache Miss! Calling API...")
    data = get_user_from_api(user_id)

    cache.set(key, data, ttl=60)

    print(f"Cache Set! Took {(time.perf_counter() - start)*1000:.3f} ms")
    return data


print(get_user(1))
print(get_user(1))