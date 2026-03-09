"""
状态机
"""

from typing import Dict, Set, Callable, Optional
from enum import Enum


class StateMachine:
    """状态机"""
    
    def __init__(self, initial_state: str):
        self.current_state = initial_state
        self.initial_state = initial_state
        self.transitions: Dict[str, Dict[str, str]] = {}
        self.handlers: Dict[str, Callable] = {}
    
    def add_transition(self, from_state: str, to_state: str, event: str):
        """添加状态转换"""
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state
    
    def on(self, state: str):
        """状态进入处理"""
        def decorator(func: Callable):
            self.handlers[state] = func
            return func
        return decorator
    
    def trigger(self, event: str) -> bool:
        """触发事件"""
        if self.current_state not in self.transitions:
            return False
        
        if event not in self.transitions[self.current_state]:
            return False
        
        new_state = self.transitions[self.current_state][event]
        self.current_state = new_state
        
        # 调用状态处理器
        if new_state in self.handlers:
            self.handlers[new_state]()
        
        return True
    
    def reset(self):
        """重置状态"""
        self.current_state = self.initial_state
    
    @property
    def state(self) -> str:
        return self.current_state


# 示例
"""
machine = StateMachine("idle")
machine.add_transition("idle", "loading", "start")
machine.add_transition("loading", "ready", "complete")
machine.add_transition("ready", "idle", "reset")

@machine.on("loading")
def loading():
    print("加载中...")

machine.trigger("start")  # -> loading
machine.trigger("complete")  # -> ready
"""
