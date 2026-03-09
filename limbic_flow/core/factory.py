"""
工厂模式
"""

from typing import Dict, Type


class EmotionFactory:
    """情绪工厂"""
    
    _creators: Dict[str, Type] = {}
    
    @classmethod
    def register(cls, name: str, creator_cls: Type):
        cls._creators[name] = creator_cls
    
    @classmethod
    def create(cls, name: str, **kwargs):
        if name not in cls._creators:
            raise ValueError(f"Unknown emotion type: {name}")
        return cls._creators[name](**kwargs)


class Registry:
    """注册表"""
    
    def __init__(self):
        self._items: Dict = {}
    
    def register(self, name: str, item):
        self._items[name] = item
    
    def get(self, name: str):
        return self._items.get(name)
    
    def list_all(self):
        return list(self._items.keys())


# 使用示例
class JoyEmotion:
    def __init__(self, **kwargs):
        self.name = "joy"

EmotionFactory.register("joy", JoyEmotion)

if __name__ == "__main__":
    emotion = EmotionFactory.create("joy")
    print(emotion.name)
