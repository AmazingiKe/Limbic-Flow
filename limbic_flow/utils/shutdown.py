"""
优雅关闭处理器
"""

import atexit
import signal
import sys
from typing import Callable, List


class GracefulShutdown:
    """优雅关闭处理器"""
    
    def __init__(self):
        self._handlers: List[Callable] = []
        self._running = True
        self._register_signals()
        atexit.register(self._cleanup)
    
    def _register_signals(self):
        """注册信号处理器"""
        if sys.platform != 'win32':
            signal.signal(signal.SIGTERM, self._signal_handler)
            signal.signal(signal.SIGINT, self._signal_handler)
        else:
            # Windows
            signal.signal(signal.SIGBREAK, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print("\n收到关闭信号，正在优雅关闭...")
        self.shutdown()
    
    def _cleanup(self):
        """清理"""
        for handler in self._handlers:
            try:
                handler()
            except Exception as e:
                print(f"清理错误: {e}")
    
    def register(self, handler: Callable):
        """注册关闭处理函数"""
        self._handlers.append(handler)
    
    def shutdown(self):
        """关闭"""
        self._running = False
        self._cleanup()
        sys.exit(0)


# 全局实例
_shutdown_handler = GracefulShutdown()


def register_shutdown_handler(handler: Callable):
    """注册关闭处理函数"""
    _shutdown_handler.register(handler)
