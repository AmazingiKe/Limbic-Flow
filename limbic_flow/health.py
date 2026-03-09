"""
健康检查
"""

import time
import psutil
from typing import Dict, Any


class HealthChecker:
    """健康检查"""
    
    @staticmethod
    def check() -> Dict[str, Any]:
        """执行健康检查"""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "system": HealthChecker._check_system(),
            "memory": HealthChecker._check_memory(),
        }
    
    @staticmethod
    def _check_system() -> Dict:
        """检查系统"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
        }
    
    @staticmethod
    def _check_memory() -> Dict:
        """检查内存"""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
        }


def health_check() -> Dict[str, Any]:
    """便捷健康检查"""
    return HealthChecker.check()
