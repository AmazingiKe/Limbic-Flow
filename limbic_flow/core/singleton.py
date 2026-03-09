"""
单例模式
"""

class SingletonMeta(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class EmotionManager(metaclass=SingletonMeta):
    """情绪管理器 (单例)"""
    def __init__(self):
        self.state = {}
    
    def set_state(self, state):
        self.state = state
    
    def get_state(self):
        return self.state


# 使用示例
m1 = EmotionManager()
m2 = EmotionManager()
print(m1 is m2)  # True
