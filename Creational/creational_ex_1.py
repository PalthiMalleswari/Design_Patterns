"""
Real-World Examples of Singleton
Singleton is useful in scenarios like:

1.Managing Shared Resources (database connections, thread pools, caches, configuration settings)
2.Coordinating System-Wide Actions (logging, print spoolers, file managers)
3.Managing State (user session, application state)


Specific Examples:

1. Logger Classes: Many logging frameworks use the Singleton pattern to provide a global logging object. This ensures that log messages are consistently handled and written to the same output stream.
2. Database Connection Pools: Connection pools help manage and reuse database connections efficiently. A Singleton can ensure that only one pool is created and used throughout the application.
3. Cache Objects: In-memory caches are often implemented as Singletons to provide a single point of access for cached data across the application.
4. Thread Pools: Thread pools manage a collection of worker threads. A Singleton ensures that the same pool is used throughout the application, preventing resource overuse.
5. File System: File systems often use Singleton objects to represent the file system and provide a unified interface for file operations.

"""


## ==================== 1. Lazy Singleton ============

"""
1.New Method(returns object for called class) will be called before init 
2.Not a ThreadSafe

"""

class LazySingletone:

    _instance = None

    def __new__(cls):
        
        if cls._instance is None:
            print("Creating a Instance")
            cls._instance = super().__new__(cls)

            return cls._instance
        else:
            print("Returning previous Instance")
            return cls._instance
    
o1 = LazySingletone()

o2 = LazySingletone()

o3 = LazySingletone()


#================ 2. Thread-Safe Singletone ===============

import threading

class ThreadSafeSingletone :

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        
        if cls._instance is None:
            
            with cls._lock:
                print("Lock is",cls._lock)
                
                if cls._instance is None: # Dobule Checking

                    cls._instance = super().__new__(cls)
                    print("Returning New Instance")
                    return cls._instance
                
        else:

            print("Returning Previous Instance")

        return cls._instance
        


#================ 3.Singleton Using a Metaclass  ===============

"""
1. Reusable to any class
2. Thread-Safe
"""

class SingletonMeta(type):

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:

            with cls._lock:

                if cls not in cls._instances:

                    cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
        


class MySingleton(metaclass=SingletonMeta):
    pass


instances = []

def create_instance():
    
    instance = MySingleton()
    instances.append(instance)

threads = []

for _ in range(10):

    t = threading.Thread(target=create_instance)
    threads.append(t)
    t.start()

for t in threads:

    t.join()

unique_instances = set(id(i) for i in instances)

print("Unique Instances ",unique_instances)


#==================== 4. Singleton via Decarator ==============


def singleton(cls):

    instances = {}

    def get_instance(*args,**kwargs):

        if cls not in instances:

            instances[cls] = cls(*args,**kwargs)
        print("Instance Created")
        return instances[cls]
    
    return get_instance

@singleton
class DBConnection:

    def __init__(self,con):
        print("Intialized the Obj ")
        self.conn = con

    def read_operation(self):

        print(f"Reading through {id(self)}")

c1 = DBConnection("con1")
c2 = DBConnection("con2")

print(c1)
print(c2)
    
# Check Which Objects used for Read operation
c1.read_operation() ## reads through con1
c2.read_operation()

print(f"c1 Connection name {c1.conn}")
print(f"c2 Connection name {c2.conn}") ## con1

## ================== 5. Borg Pattern =================

"""

The Borg Pattern  is a variation of the Singleton pattern.
But instead of forcing a single instance, it allows multiple instances,
while making them all share the same internal state.

"""

class Borg:

    _shared_state = {}

    def __new__(cls,*args,**kwargs):
        
        obj = super().__new__(cls)

        obj.__dict__ = cls._shared_state

        return obj
    
class Settings(Borg):

    def __init__(self,config):
        
        self.config = config

s1 = Settings("Conf_1")
s2 = Settings("Conf_2")

s1.l = 90

print(s2.config) ## prints Conf_2
print(s2.l) ## prints 90

## ============== 6. Eager Singleton =======================

"""
1. Instance created even if unused
2. Automatically thread-safe
3.Instance ready immediately.

"""


class EagerSingleton:

    pass

eager = EagerSingleton()


## ========== 7. Enum Singleton =================

from enum import Enum

class EnumSingleton(Enum):
    INSTANCE = object()

s = EnumSingleton.INSTANCE

print(s) ## prints EnumSingleton.INSTANCE
