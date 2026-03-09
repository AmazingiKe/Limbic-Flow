"""
事件系统
"""

from typing import Callable, Dict, List
from dataclasses import dataclass


@dataclass
class EmotionEvent:
    """情绪事件"""
    type: str
    data: Dict
    timestamp: float


class EmotionEventBus:
    """情绪事件总线"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def publish(self, event: EmotionEvent):
        """发布事件"""
        if event.type in self.listeners:
            for callback in self.listeners[event.type]:
                callback(event)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """取消订阅"""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)


class EventDrivenEmotion:
    """事件驱动情绪"""
    
    def __init__(self):
        self.event_bus = EmotionEventBus()
        self._setup_default_listeners()
    
    def _setup_default_listeners(self):
        """设置默认监听器"""
        self.event_bus.subscribe("emotion_change", self._on_emotion_change)
    
    def _on_emotion_change(self, event: EmotionEvent):
        """情绪变化处理"""
        print(f"Emotion changed: {event.data}")


if __name__ == "__main__":
    bus = EmotionEventBus()
    bus.subscribe("test", lambda e: print(e))
    bus.publish(EmotionEvent("test", {"data": "value"}, 0))
