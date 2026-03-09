"""
缓存系统
"""

import time
import hashlib
import json
from typing import Any, Callable, Optional


class Cache:
    """简单内存缓存"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 100):
        self.ttl = ttl  # 过期时间(秒)
        self.max_size = max_size
        self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        # 清理过期或满时清理
        if len(self._cache) >= self.max_size:
            # 删除最老的
            oldest = min(self._cache.items(), key=lambda x: x[1][1])
            del self._cache[oldest[0]]
        
        self._cache[key] = (value, time.time())
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """检查是否存在"""
        return self.get(key) is not None


class LRUCache:
    """LRU 缓存"""
    
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self._cache = {}
        self._order = []
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            # 移到末尾
            self._order.remove(key)
            self._order.append(key)
            return self._cache[key]
        return None
    
    def put(self, key: str, value: Any):
        if key in self._cache:
            self._order.remove(key)
        elif len(self._cache) >= self.capacity:
            oldest = self._order.pop(0)
            del self._cache[oldest]
        
        self._cache[key] = value
        self._order.append(key)
    
    def clear(self):
        self._cache.clear()
        self._order.clear()


def cache_key(*args, **kwargs) -> str:
    """生成缓存键"""
    data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()


# 全局缓存实例
_cache = Cache()


def cached(ttl: int = 3600):
    """缓存装饰器"""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            result = _cache.get(key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            _cache.set(key, result)
            return result
        
        return wrapper
    return decorator
