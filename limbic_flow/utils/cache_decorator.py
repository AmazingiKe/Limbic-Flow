"""
缓存装饰器
"""

import time
import functools
from typing import Callable, Any, Optional


def cached(ttl: int = 300, maxsize: int = 128):
    """缓存装饰器"""
    cache = {}
    cache_time = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            
            if key in cache:
                if now - cache_time[key] < ttl:
                    return cache[key]
            
            result = func(*args, **kwargs)
            
            # 限制缓存大小
            if len(cache) >= maxsize:
                oldest = min(cache_time.items(), key=lambda x: x[1])
                del cache[oldest[0]]
                del cache_time[oldest[0]]
            
            cache[key] = result
            cache_time[key] = now
            
            return result
        return wrapper
    return decorator


def memoized(func: Callable) -> Callable:
    """记忆化装饰器"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


class Cache:
    """简单缓存"""
    
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.cache = {}
        self.times = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if time.time() - self.times[key] < self.ttl:
                return self.cache[key]
            del self.cache[key]
            del self.times[key]
        return None
    
    def set(self, key: str, value: Any):
        self.cache[key] = value
        self.times[key] = time.time()
    
    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]
            del self.times[key]
    
    def clear(self):
        self.cache.clear()
        self.times.clear()
