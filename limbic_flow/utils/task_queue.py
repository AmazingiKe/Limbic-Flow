"""
异步任务队列
"""

import asyncio
from typing import Callable, Any, Dict
from dataclasses import dataclass, field
from enum import Enum
import time
import uuid


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    func: Callable
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = None
    created_at: float = field(default_factory=time.time)
    completed_at: float = None


class TaskQueue:
    """异步任务队列"""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.tasks: Dict[str, Task] = {}
        self.queue = asyncio.Queue()
        self.workers = []
    
    async def submit(self, func: Callable, *args, **kwargs) -> str:
        """提交任务"""
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            func=func,
            args=args,
            kwargs=kwargs
        )
        
        self.tasks[task_id] = task
        await self.queue.put(task)
        
        return task_id
    
    async def worker(self, worker_id: int):
        """工作协程"""
        while True:
            task = await self.queue.get()
            
            task.status = TaskStatus.Running
            
            try:
                if asyncio.iscoroutinefunction(task.func):
                    task.result = await task.func(*task.args, **task.kwargs)
                else:
                    task.result = task.func(*task.args, **task.kwargs)
                
                task.status = TaskStatus.COMPLETED
            except Exception as e:
                task.error = str(e)
                task.status = TaskStatus.FAILED
            
            task.completed_at = time.time()
            self.queue.task_done()
    
    async def start(self):
        """启动工作协程"""
        for i in range(self.max_workers):
            worker = asyncio.create_task(self.worker(i))
            self.workers.append(worker)
    
    async def stop(self):
        """停止工作协程"""
        for worker in self.workers:
            worker.cancel()
    
    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)
    
    def get_result(self, task_id: str) -> Any:
        task = self.tasks.get(task_id)
        if task:
            return task.result
        return None
