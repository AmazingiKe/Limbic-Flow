"""
敏感词过滤
"""

import re
from typing import List


class WordFilter:
    """敏感词过滤器"""
    
    def __init__(self):
        self.sensitive_words: set = set()
    
    def add_word(self, word: str):
        self.sensitive_words.add(word.lower())
    
    def add_words(self, words: List[str]):
        for word in words:
            self.add_word(word)
    
    def filter(self, text: str, replace: str = "*") -> str:
        """过滤敏感词"""
        result = text
        for word in self.sensitive_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            result = pattern.sub(replace * len(word), result)
        return result
    
    def contains(self, text: str) -> bool:
        """检查是否包含敏感词"""
        text_lower = text.lower()
        return any(word in text_lower for word in self.sensitive_words)
    
    def get_words(self, text: str) -> List[str]:
        """获取文本中的敏感词"""
        text_lower = text.lower()
        return [word for word in self.sensitive_words if word in text_lower]


# 默认敏感词
DEFAULT_SENSITIVE_WORDS = [
    # 政治相关
    "作弊", "赌博", "毒品",
    # 诈骗相关
    "钓鱼", "木马", "病毒",
]


filter_instance = WordFilter()
filter_instance.add_words(DEFAULT_SENSITIVE_WORDS)
