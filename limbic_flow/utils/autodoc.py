"""
自动文档生成
"""

import inspect
from typing import Callable, Any, Dict, List


def generate_doc_from_function(func: Callable) -> Dict[str, Any]:
    """从函数生成文档"""
    
    return {
        "name": func.__name__,
        "doc": func.__doc__,
        "signature": str(inspect.signature(func)),
        "module": func.__module__,
    }


def generate_doc_from_class(cls: type) -> Dict[str, Any]:
    """从类生成文档"""
    
    methods = {}
    for name in dir(cls):
        attr = getattr(cls, name)
        if callable(attr) and not name.startswith('_'):
            methods[name] = generate_doc_from_function(attr)
    
    return {
        "name": cls.__name__,
        "doc": cls.__doc__,
        "module": cls.__module__,
        "methods": methods,
    }


def generate_api_docs(classes: List[type]) -> Dict[str, Any]:
    """生成 API 文档"""
    
    docs = {}
    for cls in classes:
        docs[cls.__name__] = generate_doc_from_class(cls)
    
    return docs
