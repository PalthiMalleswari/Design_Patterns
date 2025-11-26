"""

 Implement a Thread-Safe Singleton Cache Manager

"""


import threading
import time

class SingletonCache:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        
        if not cls._instance:

            with cls._lock:

                if not cls._instance:

                    cls._instance = super().__new__(cls)
                    cls._instance.cache = {}
                    cls._instance.ttl   = {}

        return cls._instance
    

    def set(self,key,value,expire_in=None):

        self.cache[key] = value

        if expire_in:

            self.ttl[key] = time.time() + expire_in
    
    def get(self,key):

        # Check TTL Expiry

        if key in self.ttl and self.ttl[key] < time.time():

            self.delete(key)
            return None
        return self.cache.get(key)
    
    def delete(self,key):

        self.cache.pop(key,None)

        print(f"Deleting {key} Key")

        self.ttl.pop(key,None)
    
    def clear(self):

        self.cache.clear()

        self.ttl.clear()

# Sample Usage


cache = SingletonCache()

cache.set("user_1_profile",{"name":"John"},expire_in=60)

data = cache.get("user_1_profile")

print("Responce From Cache ",data)


"""
View: Fetch user details (expensive DB query)
"""

import time



def user_profile_view(request,user_id):

    start = time.perf_counter()

    cache_key = f"user_profile_{user_id}"

    cached = cache.get(cache_key)

    if cached:

        duration = (time.perf_counter() - start) * 1000

        return {
            "source": "singleton-cache",
            "data": cached,
            "time_ms": f"{duration:.4f}"
        }

    time.sleep(2)
    data = {"user_id":user_id,"name":"John Doe"}

    cache.set(cache_key,data,expire_in=60)

    duration = (time.perf_counter() - start) * 1000

    return {
        "source": "db",
        "data": data,
        "time_ms": f"{duration:.4f}"
    }

#Usage

u1_0 = user_profile_view("R1",123)

u1_1 = user_profile_view("R1",123)

print(u1_0)
print(u1_1)

## Results

#{'source': 'db', 'data': {'user_id': 123, 'name': 'John Doe'}, 'time_ms': '2001.3788'}
#{'source': 'singleton-cache', 'data': {'user_id': 123, 'name': 'John Doe'}, 'time_ms': '0.0119'}
