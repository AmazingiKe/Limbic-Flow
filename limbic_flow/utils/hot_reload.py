"""
热重载
"""

import importlib
import sys
from pathlib import Path


class HotReloader:
    """模块热重载"""
    
    def __init__(self):
        self.modules = {}
    
    def watch(self, module_name: str):
        """监控模块"""
        if module_name not in sys.modules:
            return
        
        self.modules[module_name] = sys.modules[module_name]
    
    def reload(self, module_name: str):
        """重载模块"""
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
            print(f"重载: {module_name}")
    
    def reload_all(self):
        """重载所有监控的模块"""
        for name in self.modules:
            self.reload(name)


reloader = HotReloader()
