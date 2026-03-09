"""
依赖检查
"""

import importlib
import sys
from typing import List, Tuple


def check_dependency(name: str) -> Tuple[bool, str]:
    """检查依赖是否安装"""
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, '__version__', 'unknown')
        return True, version
    except ImportError:
        return False, None


def check_all_dependencies() -> dict:
    """检查所有依赖"""
    deps = {
        'fastapi': 'Web 框架',
        'uvicorn': 'ASGI 服务器',
        'numpy': '数值计算',
        'pydantic': '数据验证',
        'psutil': '系统监控',
    }
    
    results = {}
    for name, desc in deps.items():
        installed, version = check_dependency(name)
        results[name] = {
            'description': desc,
            'installed': installed,
            'version': version,
        }
    
    return results


def install_missing():
    """安装缺失的依赖"""
    import subprocess
    
    required = [
        'fastapi',
        'uvicorn',
        'numpy',
        'pydantic',
        'psutil',
    ]
    
    for name in required:
        installed, _ = check_dependency(name)
        if not installed:
            print(f"安装 {name}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', name])
