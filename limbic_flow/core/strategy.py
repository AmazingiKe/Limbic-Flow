"""
策略模式
"""

from typing import Dict, Callable


class EmotionStrategy:
    """情绪策略"""
    def execute(self, context: Dict):
        pass


class PositiveStrategy(EmotionStrategy):
    def execute(self, context: Dict):
        return {"emotion": "positive", "intensity": 0.8}


class NegativeStrategy(EmotionStrategy):
    def execute(self, context: Dict):
        return {"emotion": "negative", "intensity": 0.6}


class StrategyContext:
    """策略上下文"""
    def __init__(self):
        self.strategies: Dict[str, EmotionStrategy] = {}
    
    def set_strategy(self, name: str, strategy: EmotionStrategy):
        self.strategies[name] = strategy
    
    def execute(self, name: str, context: Dict) -> Dict:
        if name in self.strategies:
            return self.strategies[name].execute(context)
        return {}


# 使用示例
ctx = StrategyContext()
ctx.set_strategy("happy", PositiveStrategy())
ctx.set_strategy("sad", NegativeStrategy())
result = ctx.execute("happy", {})
print(result)
