"""
观察者模式
"""

from typing import Callable, List, Any, Dict
from dataclasses import dataclass, field


@dataclass
class Observer:
    """观察者"""
    callback: Callable
    name: str = ""
    priority: int = 0


class Observable:
    """可观察对象"""
    
    def __init__(self):
        self.observers: List[Observer] = []
    
    def subscribe(self, callback: Callable, name: str = "", priority: int = 0):
        """订阅"""
        observer = Observer(callback, name, priority)
        self.observers.append(observer)
        # 按优先级排序
        self.observers.sort(key=lambda x: x.priority, reverse=True)
    
    def unsubscribe(self, name: str):
        """取消订阅"""
        self.observers = [o for o in self.observers if o.name != name]
    
    def notify(self, *args, **kwargs):
        """通知所有观察者"""
        for observer in self.observers:
            observer.callback(*args, **kwargs)


class EventEmitter:
    """事件发射器"""
    
    def __init__(self):
        self.events: Dict[str, Observable] = {}
    
    def on(self, event: str, callback: Callable, name: str = ""):
        """注册事件"""
        if event not in self.events:
            self.events[event] = Observable()
        self.events[event].subscribe(callback, name)
    
    def off(self, event: str, name: str = ""):
        """取消事件"""
        if event in self.events:
            self.events[event].unsubscribe(name)
    
    def emit(self, event: str, *args, **kwargs):
        """发射事件"""
        if event in self.events:
            self.events[event].notify(*args, **kwargs)


# 全局事件发射器
events = EventEmitter()
