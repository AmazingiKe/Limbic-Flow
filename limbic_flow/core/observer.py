"""
观察者模式实现
"""

from typing import Callable, List
from dataclasses import dataclass


@dataclass
class Observer:
    """观察者"""
    id: str
    callback: Callable


class Subject:
    """主题"""
    
    def __init__(self):
        self.observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self.observers.append(observer)
    
    def detach(self, observer_id: str):
        self.observers = [o for o in self.observers if o.id != observer_id]
    
    def notify(self, data):
        for observer in self.observers:
            observer.callback(data)


class EmotionSubject(Subject):
    """情绪主题"""
    
    def __init__(self):
        super().__init__()
        self._current_emotion = {}
    
    @property
    def emotion(self):
        return self._current_emotion
    
    @emotion.setter
    def emotion(self, value):
        old = self._current_emotion
        self._current_emotion = value
        self.notify({"old": old, "new": value})


# 使用示例
def on_emotion_change(data):
    print(f"Emotion changed: {data}")

subject = EmotionSubject()
subject.attach(Observer("1", on_emotion_change))
subject.emotion = {"joy": 0.8}
