"""
任务调度
"""

import asyncio
from typing import Callable, Dict, List
from dataclasses import dataclass, field
import time


@dataclass
class Task:
    """任务"""
    id: str
    func: Callable
    interval: int = 0  # 0 表示只执行一次
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    last_run: float = 0
    enabled: bool = True


class Scheduler:
    """任务调度器"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task_id: str, func: Callable, interval: int = 0):
        """添加任务"""
        self.tasks[task_id] = Task(
            id=task_id,
            func=func,
            interval=interval
        )
    
    async def run(self):
        """运行调度器"""
        while True:
            now = time.time()
            for task in self.tasks.values():
                if not task.enabled:
                    continue
                if task.interval == 0:
                    # 只执行一次
                    if task.last_run == 0:
                        task.func(*task.args, **task.kwargs)
                        task.last_run = now
                else:
                    # 周期性执行
                    if now - task.last_run >= task.interval:
                        task.func(*task.args, **task.kwargs)
                        task.last_run = now
            
            await asyncio.sleep(1)
    
    def enable(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True
    
    def disable(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False
