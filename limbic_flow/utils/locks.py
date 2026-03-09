"""
信号量与并发控制
"""

import asyncio
import threading
from typing import Optional, Any
from contextlib import asynccontextmanager, contextmanager


class Semaphore:
    """信号量"""
    
    def __init__(self, value: int = 1):
        self.value = value
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    
    def acquire(self, blocking: bool = True):
        """获取信号"""
        with self.condition:
            while self.value == 0:
                if not blocking:
                    return False
                self.condition.wait()
            self.value -= 1
            return True
    
    def release(self):
        """释放信号"""
        with self.condition:
            self.value += 1
            self.condition.notify()
    
    @contextmanager
    def __call__(self):
        self.acquire()
        try:
            yield
        finally:
            self.release()


class AsyncSemaphore:
    """异步信号量"""
    
    def __init__(self, value: int = 1):
        self.value = value
        self.condition = asyncio.Condition()
    
    async def acquire(self):
        async with self.condition:
            while self.value == 0:
                await self.condition.wait()
            self.value -= 1
    
    async def release(self):
        async with self.condition:
            self.value += 1
            self.condition.notify()
    
    @asynccontextmanager
    async def __call__(self):
        await self.acquire()
        try:
            yield
        finally:
            await self.release()


class Lock:
    """线程锁"""
    
    def __init__(self):
        self.lock = threading.Lock()
    
    @contextmanager
    def __call__(self):
        with self.lock:
            yield


class AsyncLock:
    """异步锁"""
    
    def __init__(self):
        self.lock = asyncio.Lock()
    
    @asynccontextmanager
    async def __call__(self):
        async with self.lock:
            yield
