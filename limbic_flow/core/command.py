"""
命令模式
"""

from typing import Callable, Any


class Command:
    """命令基类"""
    def execute(self):
        pass


class EmotionCommand(Command):
    """情绪命令"""
    def __init__(self, receiver, action: str, params: Any):
        self.receiver = receiver
        self.action = action
        self.params = params
    
    def execute(self):
        if self.action == "set":
            self.receiver.set_state(self.params)
        elif self.action == "update":
            self.receiver.update(self.params)


class CommandQueue:
    """命令队列"""
    def __init__(self):
        self.queue = []
    
    def add(self, command: Command):
        self.queue.append(command)
    
    def execute_all(self):
        while self.queue:
            cmd = self.queue.pop(0)
            cmd.execute()


# 使用示例
class EmotionReceiver:
    def set_state(self, state):
        print(f"Set state: {state}")
    
    def update(self, update):
        print(f"Update: {update}")


receiver = EmotionReceiver()
cmd = EmotionCommand(receiver, "set", {"joy": 0.8})
cmd.execute()
