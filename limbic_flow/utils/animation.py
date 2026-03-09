"""
动画效果
"""

import time
from typing import Callable


class Animator:
    """简单动画"""
    
    @staticmethod
    def typewriter(text: str, delay: float = 0.05):
        """打字机效果"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def progress_bar(current: int, total: int, width: int = 30):
        """进度条"""
        percent = current / total
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        print(f'\r[{bar}] {percent*100:.1f}%', end='', flush=True)


def loading_animation(text: str = "加载中"):
    """加载动画"""
    chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    i = 0
    while True:
        print(f'\r{chars[i % len(chars)]} {text}', end='', flush=True)
        time.sleep(0.1)
        i += 1
