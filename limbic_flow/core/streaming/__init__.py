"""
流式输出模块

功能：
- 提供分段输出的能力
- 支持不同的输出策略
- 可与各种前端集成
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable, List, Dict, Any
import time
import sys


class StreamingOutput(ABC):
    """
    流式输出抽象基类
    
    设计原则：
    - 依赖倒置：高层模块依赖此抽象接口，不依赖具体实现
    - 开闭原则：新增输出策略只需继承此类，无需修改现有代码
    - 单一职责：每个实现只负责一种输出策略
    """
    
    @abstractmethod
    def write(self, content: str) -> None:
        """
        写入内容
        
        Args:
            content: 要写入的内容
        """
        pass
    
    @abstractmethod
    def flush(self) -> None:
        """
        刷新缓冲区
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """
        关闭输出
        """
        pass


class ConsoleStreamingOutput(StreamingOutput):
    """
    控制台流式输出实现
    """
    
    def __init__(self, chunk_size: int = 50, delay: float = 0.01):
        """
        初始化控制台流式输出
        
        Args:
            chunk_size: 每段输出的字符数
            delay: 每段输出之间的延迟（秒）
        """
        self.chunk_size = chunk_size
        self.delay = delay
        self.buffer = ""
    
    def write(self, content: str) -> None:
        """
        写入内容到控制台
        
        Args:
            content: 要写入的内容
        """
        self.buffer += content
        
        # 当缓冲区达到指定大小时，分段输出
        while len(self.buffer) >= self.chunk_size:
            chunk = self.buffer[:self.chunk_size]
            self.buffer = self.buffer[self.chunk_size:]
            print(chunk, end="", flush=True)
            time.sleep(self.delay)
    
    def flush(self) -> None:
        """
        刷新缓冲区
        """
        if self.buffer:
            print(self.buffer, end="", flush=True)
            self.buffer = ""
    
    def close(self) -> None:
        """
        关闭输出
        """
        self.flush()


class CallbackStreamingOutput(StreamingOutput):
    """
    回调函数流式输出实现
    
    用于与前端或其他系统集成
    """
    
    def __init__(self, callback: Callable[[str], None], chunk_size: int = 50, delay: float = 0.01):
        """
        初始化回调函数流式输出
        
        Args:
            callback: 回调函数，接收分段内容
            chunk_size: 每段输出的字符数
            delay: 每段输出之间的延迟（秒）
        """
        self.callback = callback
        self.chunk_size = chunk_size
        self.delay = delay
        self.buffer = ""
    
    def write(self, content: str) -> None:
        """
        写入内容到回调函数
        
        Args:
            content: 要写入的内容
        """
        self.buffer += content
        
        # 当缓冲区达到指定大小时，分段输出
        while len(self.buffer) >= self.chunk_size:
            chunk = self.buffer[:self.chunk_size]
            self.buffer = self.buffer[self.chunk_size:]
            self.callback(chunk)
            time.sleep(self.delay)
    
    def flush(self) -> None:
        """
        刷新缓冲区
        """
        if self.buffer:
            self.callback(self.buffer)
            self.buffer = ""
    
    def close(self) -> None:
        """
        关闭输出
        """
        self.flush()


class StreamingManager:
    """
    流式输出管理器
    
    负责管理流式输出的生命周期
    """
    
    def __init__(self, output: Optional[StreamingOutput] = None):
        """
        初始化流式输出管理器
        
        Args:
            output: 流式输出实例，如果为 None，则使用默认的控制台输出
        """
        self.output = output or ConsoleStreamingOutput()
    
    def stream(self, generator_func: Callable[[Callable[[str], None]], str]) -> str:
        """
        流式处理生成器函数
        
        Args:
            generator_func: 生成器函数，接收一个回调函数作为参数
        
        Returns:
            str: 完整的生成内容
        """
        def callback(content: str):
            self.output.write(content)
        
        try:
            full_content = generator_func(callback)
            self.output.flush()
            return full_content
        finally:
            self.output.close()
    
    def create_streaming_callback(self) -> Callable[[str], None]:
        """
        创建流式回调函数
        
        Returns:
            Callable[[str], None]: 流式回调函数
        """
        def callback(content: str):
            self.output.write(content)
        
        return callback


def create_streaming_output(output_type: str = "console", **kwargs) -> StreamingOutput:
    """
    创建流式输出实例
    
    Args:
        output_type: 输出类型，支持 "console" 和 "callback"
        **kwargs: 额外的参数
        
    Returns:
        StreamingOutput: 流式输出实例
    """
    if output_type == "console":
        return ConsoleStreamingOutput(**kwargs)
    elif output_type == "callback":
        callback = kwargs.get("callback")
        if not callback:
            raise ValueError("Callback is required for callback output type")
        return CallbackStreamingOutput(callback, **kwargs)
    else:
        raise ValueError(f"Unsupported output type: {output_type}")


def stream_to_console(generator_func: Callable[[Callable[[str], None]], str], **kwargs) -> str:
    """
    流式输出到控制台的便捷函数
    
    Args:
        generator_func: 生成器函数，接收一个回调函数作为参数
        **kwargs: 额外的参数，传递给 ConsoleStreamingOutput
        
    Returns:
        str: 完整的生成内容
    """
    output = ConsoleStreamingOutput(**kwargs)
    manager = StreamingManager(output)
    return manager.stream(generator_func)
