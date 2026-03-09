"""
事件系统 - 用于模块间解耦通信

[用途]
- Pipeline 各阶段的事件通知
- 插件化的钩子机制
- 调试和监控
"""

from typing import Callable, Dict, List, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class EventType(Enum):
    """事件类型"""
    # Pipeline 事件
    PIPELINE_START = "pipeline_start"
    PIPELINE_END = "pipeline_end"
    
    # 认知事件
    PERCEPTION = "perception"
    EMOTION_UPDATE = "emotion_update"
    MEMORY_RETRIEVED = "memory_retrieved"
    MEMORY_STORED = "memory_stored"
    PATHOLOGY_APPLIED = "pathology_applied"
    THINKING = "thinking"
    EXPRESSION = "expression"
    
    # 错误事件
    ERROR = "error"


@dataclass
class Event:
    """事件对象"""
    type: EventType
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def __str__(self):
        return f"Event({self.type.value}, data={self.data})"


class EventHandler:
    """事件处理器"""
    
    def __init__(self, callback: Callable[[Event], None]):
        self.callback = callback
    
    def __call__(self, event: Event):
        self.callback(event)


class EventBus:
    """
    事件总线 - 简单的发布订阅实现
    
    [用途]
    - 各模块可以订阅感兴趣的事件
    - Pipeline 在关键节点发布事件
    - 便于调试和扩展
    """
    
    def __init__(self):
        self._subscribers: Dict[EventType, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []
        self._event_history: List[Event] = []
        self._max_history = 100
    
    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]) -> EventHandler:
        """
        订阅事件
        
        Args:
            event_type: 事件类型
            handler: 处理函数
        
        Returns:
            订阅句柄，可用于取消订阅
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        
        event_handler = EventHandler(handler)
        self._subscribers[event_type].append(event_handler)
        return event_handler
    
    def subscribe_all(self, handler: Callable[[Event], None]) -> EventHandler:
        """
        订阅所有事件
        
        Args:
            handler: 处理函数
        
        Returns:
            订阅句柄
        """
        event_handler = EventHandler(handler)
        self._global_handlers.append(event_handler)
        return event_handler
    
    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """
        取消订阅
        
        Args:
            event_type: 事件类型
            handler: 订阅句柄
        """
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
            except ValueError:
                pass
    
    def publish(self, event: Event) -> None:
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
        if event.type in self._subscribers:
            for handler in self._subscribers[event.type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Event handler error: {e}")
        
        # 通知全局订阅者
        for handler in self._global_handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Global event handler error: {e}")
    
    def get_history(self, event_type: EventType = None, limit: int = 10) -> List[Event]:
        """
        获取事件历史
        
        Args:
            event_type: 过滤类型（可选）
            limit: 返回数量
        
        Returns:
            事件列表
        """
        history = self._event_history
        
        if event_type:
            history = [e for e in history if e.type == event_type]
        
        return history[-limit:]
    
    def clear_history(self) -> None:
        """清空历史"""
        self._event_history.clear()


# 全局事件总线实例
_event_bus = None

def get_event_bus() -> EventBus:
    """获取全局事件总线"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


# 便捷装饰器
def on_event(event_type: EventType):
    """
    事件订阅装饰器
    
    Example:
        @on_event(EventType.EMOTION_UPDATE)
        def handle_emotion(event):
            print(f"Emotion updated: {event.data}")
    """
    def decorator(func: Callable[[Event], None]) -> Callable[[Event], None]:
        bus = get_event_bus()
        bus.subscribe(event_type, func)
        return func
    return decorator
