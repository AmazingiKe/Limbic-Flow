"""
中间件系统 - 请求/响应处理链

参考现代 Web 框架设计:
- 请求前后处理
- 可插拔中间件
- 顺序执行
"""

from typing import Callable, List, Any, Dict, Optional
from abc import ABC, abstractmethod
import time


class Middleware(ABC):
    """中间件基类"""
    
    @abstractmethod
    async def process(self, context: Dict, next_handler: Callable):
        """
        处理请求
        
        Args:
            context: 请求上下文
            next_handler: 下一个处理函数
        """
        pass


class MiddlewareChain:
    """
    中间件链
    
    管理中间件的注册和执行顺序
    """
    
    def __init__(self):
        self.middlewares: List[Middleware] = []
    
    def use(self, middleware: Middleware):
        """添加中间件"""
        self.middlewares.append(middleware)
    
    async def execute(self, context: Dict, final_handler: Callable):
        """执行中间件链"""
        
        async def create_chain(index: int):
            if index >= len(self.middlewares):
                return await final_handler(context)
            
            middleware = self.middlewares[index]
            
            async def next_handler():
                return await create_chain(index + 1)
            
            return await middleware.process(context, next_handler)
        
        return await create_chain(0)


# 内置中间件
class LoggingMiddleware(Middleware):
    """日志中间件"""
    
    async def process(self, context: Dict, next_handler: Callable):
        start_time = time.time()
        
        print(f"→ {context.get('method', 'UNKNOWN')} {context.get('path', '/')}")
        
        try:
            result = await next_handler()
            elapsed = time.time() - start_time
            print(f"← 200 ({elapsed*1000:.1f}ms)")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"← Error: {e} ({elapsed*1000:.1f}ms)")
            raise


class TimingMiddleware(Middleware):
    """计时中间件"""
    
    async def process(self, context: Dict, next_handler: Callable):
        start = time.time()
        result = await next_handler()
        context['timing'] = time.time() - start
        return result


class ErrorHandlingMiddleware(Middleware):
    """错误处理中间件"""
    
    async def process(self, context: Dict, next_handler: Callable):
        try:
            return await next_handler()
        except Exception as e:
            context['error'] = str(e)
            return {
                "error": True,
                "message": str(e)
            }


# 便捷函数
def create_middleware_chain(middlewares: List[str] = None) -> MiddlewareChain:
    """创建中间件链"""
    chain = MiddlewareChain()
    
    middlewares = middlewares or ["logging", "timing", "error"]
    
    for name in middlewares:
        if name == "logging":
            chain.use(LoggingMiddleware())
        elif name == "timing":
            chain.use(TimingMiddleware())
        elif name == "error":
            chain.use(ErrorHandlingMiddleware())
    
    return chain
