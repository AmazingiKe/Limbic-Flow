"""
文件监控
"""

import time
from pathlib import Path
from typing import Callable, Dict


class FileWatcher:
    """文件监控"""
    
    def __init__(self):
        self.mtimes: Dict[str, float] = {}
    
    def watch(self, path: str, callback: Callable):
        """监控文件变化"""
        p = Path(path)
        
        if not p.exists():
            return
        
        mtime = p.stat().st_mtime
        
        if path not in self.mtimes:
            self.mtimes[path] = mtime
            return
        
        if mtime > self.mtimes[path]:
            self.mtimes[path] = mtime
            callback(path)
    
    def watch_dir(self, dir_path: str, callback: Callable):
        """监控目录变化"""
        p = Path(dir_path)
        
        if not p.exists():
            return
        
        for file in p.rglob("*"):
            if file.is_file():
                self.watch(str(file), callback)


def watch_files(paths: list, callback: Callable):
    """便捷的文件监控函数"""
    watcher = FileWatcher()
    
    while True:
        for path in paths:
            watcher.watch(path, callback)
        time.sleep(1)
