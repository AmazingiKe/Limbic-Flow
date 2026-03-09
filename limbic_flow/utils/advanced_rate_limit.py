"""
限流器 (令牌桶)
"""

import time
import threading
from typing import Optional


class TokenBucket:
    """令牌桶限流"""
    
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # 每秒令牌数
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
    
    def acquire(self, tokens: int = 1) -> bool:
        """获取令牌"""
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_for_token(self, tokens: int = 1):
        """等待令牌"""
        while not self.acquire(tokens):
            time.sleep(0.1)


class SlidingWindowRateLimiter:
    """滑动窗口限流"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
        self.lock = threading.Lock()
    
    def allow(self) -> bool:
        """检查是否允许请求"""
        with self.lock:
            now = time.time()
            # 清理过期请求
            self.requests = [t for t in self.requests if now - t < self.window_seconds]
            
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False


# 全局限流器
api_limiter = TokenBucket(rate=10, capacity=20)
