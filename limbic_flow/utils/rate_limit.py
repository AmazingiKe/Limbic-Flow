"""
限流器
"""

import time
from typing import Dict, Optional
from collections import defaultdict


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_requests: int = 60, window: int = 60):
        """
        Args:
            max_requests: 时间窗口内最大请求数
            window: 时间窗口(秒)
        """
        self.max_requests = max_requests
        self.window = window
        self._requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key: str = "default") -> bool:
        """检查是否允许请求"""
        now = time.time()
        
        # 清理过期记录
        self._requests[key] = [
            t for t in self._requests[key]
            if now - t < self.window
        ]
        
        # 检查限制
        if len(self._requests[key]) >= self.max_requests:
            return False
        
        # 记录请求
        self._requests[key].append(now)
        return True
    
    def get_remaining(self, key: str = "default") -> int:
        """获取剩余请求数"""
        now = time.time()
        
        # 清理过期记录
        self._requests[key] = [
            t for t in self._requests[key]
            if now - t < self.window
        ]
        
        return max(0, self.max_requests - len(self._requests[key]))
    
    def reset(self, key: str = "default"):
        """重置限制"""
        if key in self._requests:
            del self._requests[key]


class TokenBucket:
    """令牌桶算法"""
    
    def __init__(self, rate: float = 10, capacity: int = 10):
        """
        Args:
            rate: 每秒产生令牌数
            capacity: 桶容量
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """尝试消费令牌"""
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.rate
        )
        self.last_update = now


# 全局限流器
_rate_limiter = RateLimiter(max_requests=60, window=60)


def rate_limit(key: str = "default"):
    """限流装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not _rate_limiter.is_allowed(key):
                raise Exception("请求过于频繁，请稍后再试")
            return func(*args, **kwargs)
        return wrapper
    return decorator
