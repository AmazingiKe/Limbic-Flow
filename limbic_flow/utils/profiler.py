"""
性能分析
"""

import cProfile
import pstats
import io
from functools import wraps


def profile(func):
    """性能分析装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        result = func(*args, **kwargs)
        
        pr.disable()
        
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)
        
        print(s.getvalue())
        
        return result
    return wrapper


def timeit(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        
        result = func(*args, **kwargs)
        
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed*1000:.2f}ms")
        
        return result
    return wrapper


class Timer:
    """上下文管理器计时"""
    
    def __init__(self, name: str = ""):
        self.name = name
        self.start = None
    
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        import time
        elapsed = time.perf_counter() - self.start
        print(f"{self.name} took {elapsed*1000:.2f}ms")
