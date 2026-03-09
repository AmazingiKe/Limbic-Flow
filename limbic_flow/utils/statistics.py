"""
统计工具
"""

import math
from typing import List


def mean(values: List[float]) -> float:
    """平均值"""
    return sum(values) / len(values) if values else 0


def median(values: List[float]) -> float:
    """中位数"""
    if not values:
        return 0
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 0:
        return (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    return sorted_values[n//2]


def std(values: List[float]) -> float:
    """标准差"""
    if len(values) < 2:
        return 0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def percentile(values: List[float], p: float) -> float:
    """百分位数"""
    if not values:
        return 0
    sorted_values = sorted(values)
    k = (len(sorted_values) - 1) * p / 100
    f = int(k)
    c = f + 1 if f + 1 < len(sorted_values) else f
    return sorted_values[f] + (k - f) * (sorted_values[c] - sorted_values[f])


def histogram(values: List[float], bins: int = 10) -> dict:
    """直方图"""
    if not values:
        return {}
    
    min_val = min(values)
    max_val = max(values)
    bin_width = (max_val - min_val) / bins
    
    result = {}
    for i in range(bins):
        start = min_val + i * bin_width
        end = start + bin_width
        count = sum(1 for v in values if start <= v < end)
        result[f"{start:.2f}-{end:.2f}"] = count
    
    return result
