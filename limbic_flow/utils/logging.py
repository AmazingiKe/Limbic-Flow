"""
日志记录模块
"""

from typing import Any, Dict
import time


class EmotionLogger:
    """情绪日志记录器"""
    
    def __init__(self, log_file: str = "emotion_log.txt"):
        self.log_file = log_file
    
    def log(self, event_type: str, data: Dict[str, Any]):
        """记录事件"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event_type}: {data}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Log error: {e}")
    
    def log_emotion_change(self, old_state, new_state):
        """记录情绪变化"""
        self.log("emotion_change", {
            "old": old_state,
            "new": new_state
        })


class EmotionDebugger:
    """情绪调试器"""
    
    def __init__(self):
        self.enabled = False
    
    def debug(self, message: str, data: Any = None):
        """调试信息"""
        if self.enabled:
            print(f"[DEBUG] {message}")
            if data:
                print(f"  Data: {data}")
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False


if __name__ == "__main__":
    logger = EmotionLogger()
    logger.log_emotion_change({"joy": 0.5}, {"joy": 0.8})
