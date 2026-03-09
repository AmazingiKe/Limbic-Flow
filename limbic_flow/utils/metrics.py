"""
指标和统计
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Metrics:
    """指标数据"""
    timestamp: float = field(default_factory=time.time)
    request_count: int = 0
    error_count: int = 0
    total_latency: float = 0.0
    avg_latency: float = 0.0
    
    def add_request(self, latency: float, is_error: bool = False):
        """添加请求"""
        self.request_count += 1
        if is_error:
            self.error_count += 1
        self.total_latency += latency
        if self.request_count > 0:
            self.avg_latency = self.total_latency / self.request_count
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(1, self.request_count),
            "avg_latency": self.avg_latency,
        }


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.metrics = Metrics()
        self.request_times: List[float] = []
    
    def record_request(self, latency: float, is_error: bool = False):
        """记录请求"""
        self.metrics.add_request(latency, is_error)
        self.request_times.append(time.time())
    
    def get_metrics(self) -> Dict:
        """获取指标"""
        return self.metrics.to_dict()
    
    def reset(self):
        """重置"""
        self.metrics = Metrics()


# 全局收集器
_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    return _collector


def record_request(latency: float, is_error: bool = False):
    """记录请求"""
    _collector.record_request(latency, is_error)
