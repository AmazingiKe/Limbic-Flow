"""
类型提示
"""

from typing import TypeVar, Generic, List, Dict, Any, Optional, Callable
from dataclasses import dataclass


T = TypeVar('T')


class Result(Generic[T]):
    """结果类型"""
    
    def __init__(self, success: bool, data: T = None, error: str = ""):
        self.success = success
        self.data = data
        self.error = error
    
    @classmethod
    def ok(cls, data: T = None) -> 'Result[T]':
        return cls(True, data)
    
    @classmethod
    def err(cls, error: str) -> 'Result[T]':
        return cls(False, None, error)


@dataclass
class Page(Generic[T]):
    """分页结果"""
    items: List[T]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size
    
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        return self.page > 1


# 类型别名
JSON = Dict[str, Any]
Callback = Callable[..., Any]
