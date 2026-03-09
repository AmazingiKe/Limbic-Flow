"""
分页器
"""

from typing import List, TypeVar, Generic, Optional
from dataclasses import dataclass

T = TypeVar('T')


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
    
    @property
    def next_page(self) -> Optional[int]:
        return self.page + 1 if self.has_next else None
    
    @property
    def prev_page(self) -> Optional[int]:
        return self.page - 1 if self.has_prev else None


class Paginator(Generic[T]):
    """分页器"""
    
    def __init__(self, items: List[T], page: int = 1, page_size: int = 20):
        self.items = items
        self.page = max(1, page)
        self.page_size = max(1, page_size)
    
    def paginate(self) -> Page[T]:
        """分页"""
        total = len(self.items)
        start = (self.page - 1) * self.page_size
        end = start + self.page_size
        
        return Page(
            items=self.items[start:end],
            total=total,
            page=self.page,
            page_size=self.page_size
        )
    
    def __iter__(self):
        for item in self.items:
            yield item
