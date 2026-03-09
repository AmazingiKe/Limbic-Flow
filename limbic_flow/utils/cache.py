"""
缓存模块
"""

from typing import Any, Dict, Optional
import time


class EmotionCache:
    """情绪缓存"""
    
    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self.cache: Dict[str, tuple] = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        if len(self.cache) >= self.max_size:
            # 删除最老的
            oldest = min(self.cache.items(), key=lambda x: x[1][1])
            del self.cache[oldest[0]]
        
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()


class EmotionMemoryCache:
    """情绪记忆缓存"""
    
    def __init__(self):
        self.recent_states = []
        self.max_recent = 50
    
    def add_state(self, state: Dict):
        """添加状态"""
        self.recent_states.append(state)
        if len(self.recent_states) > self.max_recent:
            self.recent_states.pop(0)
    
    def get_recent(self, count: int = 10) -> list:
        """获取最近状态"""
        return self.recent_states[-count:]


if __name__ == "__main__":
    cache = EmotionCache()
    cache.set("test", {"joy": 0.8})
    print(cache.get("test"))
