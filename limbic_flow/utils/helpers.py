"""
工具函数库
"""

import hashlib
import random
import string
import time
from typing import Any, Dict, List


def generate_id(prefix: str = "") -> str:
    """生成唯一ID"""
    timestamp = str(time.time()).replace(".", "")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}{timestamp}{random_str}"


def hash_text(text: str) -> str:
    """文本哈希"""
    return hashlib.sha256(text.encode()).hexdigest()


def safe_get(d: Dict, *keys, default=None) -> Any:
    """安全获取嵌套字典值"""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
            if d is None:
                return default
        else:
            return default
    return d if d is not None else default


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """将列表分块"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """限制值在范围内"""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """线性插值"""
    return a + (b - a) * t


def format_time(timestamp: float) -> str:
    """格式化时间"""
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    # 移除非法字符
    import re
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename


def merge_dicts(*dicts: Dict) -> Dict:
    """合并多个字典"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result
