"""
事件系统 - 模块间解耦通信

参考 AstrBot 设计:
- 事件驱动架构
- 插件钩子
- 异步事件处理
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import time


class EventType(Enum):
    """事件类型"""
    # Pipeline 事件
    PIPELINE_START = "pipeline_start"
    PIPELINE_END = "pipeline_end"
    
    # 认知事件
    USER_MESSAGE = "user_message"
    BOT_RESPONSE = "bot_response"
    
    # 情绪事件
    EMOTION_CHANGED = "emotion_changed"
    EMOTION_RESET = "emotion_reset"
    
    # 记忆事件
    MEMORY_STORED = "memory_stored"
    MEMORY_RETRIEVED = "memory_retrieved"
    
    # 错误事件
    ERROR = "error"


@dataclass
class Event:
    """事件对象"""
    type: EventType
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: str = "system"
    
    def __str__(self):
        return f"Event({self.type.value}, source={self.source})"


class EventHandler:
    """事件处理器"""
    
    def __init__(self, callback: Callable, priority: int = 0):
        self.callback = callback
        self.priority = priority
    
    async def __call__(self, event: Event):
        if asyncio.iscoroutinefunction(self.callback):
            await self.callback(event)
        else:
            self.callback(event)


class EventBus:
    """
    事件总线
    
    特点:
    - 异步支持
    - 优先级排序
    - 一次性/持久订阅
    """
    
    def __init__(self, async_mode: bool = True):
        self.async_mode = async_mode
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []
        self._event_history: List[Event] = []
        self._max_history = 100
    
    def subscribe(
        self, 
        event_type: EventType, 
        handler: Callable,
        priority: int = 0,
        one_time: bool = False
    ) -> EventHandler:
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 处理函数
            priority: 优先级 (数字越大越先执行)
            one_time: 是否只执行一次
        
        Returns:
            事件处理器
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        
        event_handler = EventHandler(handler, priority)
        event_handler.one_time = one_time
        
        self._handlers[event_type].append(event_handler)
        
        # 按优先级排序
        self._handlers[event_type].sort(key=lambda h: h.priority, reverse=True)
        
        return event_handler
    
    def unsubscribe(self, event_type: EventType, handler: EventHandler):
        """取消订阅"""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    async def publish(self, event: Event):
        """
        发布事件
        
        Args:
            event: 事件对象
        """
        # 记录历史
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)
        
        # 通知特定类型订阅者
        if event.type in self._handlers:
            handlers = self._handlers[event.type].copy()
            
            for handler in handlers:
                try:
                    await handler(event)
                except Exception as e:
                    print(f"Event handler error: {e}")
                
                # 一次性处理器
                if getattr(handler, 'one_time', False):
                    self.unsubscribe(event.type, handler)
        
        # 通知全局订阅者
        for handler in self._global_handlers:
            try:
                await handler(event)
            except Exception as e:
                print(f"Global event handler error: {e}")
    
    def on(
        self, 
        event_type: EventType, 
        priority: int = 0,
        one_time: bool = False
    ) -> Callable:
        """
        装饰器方式订阅事件
        
        Example:
            @event_bus.on(EventType.USER_MESSAGE)
            async def handle_message(event):
                print(event.data)
        """
        def decorator(func: Callable) -> Callable:
            self.subscribe(event_type, func, priority, one_time)
            return func
        return decorator
    
    def get_history(
        self, 
        event_type: EventType = None, 
        limit: int = 10
    ) -> List[Event]:
        """获取事件历史"""
        history = self._event_history
        
        if event_type:
            history = [e for e in history if e.type == event_type]
        
        return history[-limit:]


# 全局事件总线
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """获取全局事件总线"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


# 便捷装饰器
def on_event(event_type: EventType, priority: int = 0):
    """
    事件订阅装饰器
    
    Example:
        @on_event(EventType.EMOTION_CHANGED)
        def handle_emotion(event):
            print(f"Emotion changed: {event.data}")
    """
    def decorator(func: Callable) -> Callable:
        get_event_bus().subscribe(event_type, func, priority)
        return func
    return decorator
