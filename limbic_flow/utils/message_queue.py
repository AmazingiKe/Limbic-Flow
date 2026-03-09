"""
消息队列
"""

import asyncio
from typing import Any, Optional, Callable, Dict, List
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid


class MessagePriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2


@dataclass
class Message:
    """消息"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    payload: Any = None
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: float = field(default_factory=time.time)
    headers: Dict[str, str] = field(default_factory=dict)


class MessageQueue:
    """消息队列"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=max_size)
        self.subscribers: Dict[str, List[asyncio.Queue]] = {}
    
    async def put(self, message: Message):
        """发送消息"""
        # 优先级取反(越小越优先)
        priority = -message.priority.value
        await self.queue.put((priority, message))
        
        # 通知订阅者
        if message.topic in self.subscribers:
            for sub in self.subscribers[message.topic]:
                await sub.put(message)
    
    async def get(self) -> Message:
        """接收消息"""
        _, message = await self.queue.get()
        return message
    
    def subscribe(self, topic: str) -> asyncio.Queue:
        """订阅主题"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        queue = asyncio.Queue()
        self.subscribers[topic].append(queue)
        return queue
    
    def unsubscribe(self, topic: str, queue: asyncio.Queue):
        """取消订阅"""
        if topic in self.subscribers:
            self.subscribers[topic].remove(queue)


# 全局消息队列
mq = MessageQueue()
