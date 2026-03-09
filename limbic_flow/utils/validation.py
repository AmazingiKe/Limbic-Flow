"""
数据验证模块
"""

from typing import Any, Dict


class EmotionValidator:
    """情绪数据验证器"""
    
    @staticmethod
    def validate_pad(pad: Dict[str, float]) -> bool:
        """验证PAD值"""
        for key in ["pleasure", "arousal", "dominance"]:
            if key not in pad:
                return False
            if not -1 <= pad[key] <= 1:
                return False
        return True
    
    @staticmethod
    def validate_emotion(emotion: Dict[str, float]) -> bool:
        """验证情绪值"""
        for value in emotion.values():
            if not 0 <= value <= 1:
                return False
        return True


class EmotionSanitizer:
    """情绪数据清洗器"""
    
    @staticmethod
    def sanitize_pad(pad: Dict[str, float]) -> Dict[str, float]:
        """清洗PAD值"""
        sanitized = {}
        
        for key in ["pleasure", "arousal", "dominance"]:
            value = pad.get(key, 0)
            sanitized[key] = max(-1, min(1, value))
        
        return sanitized
    
    @staticmethod
    def sanitize_emotion(emotion: Dict[str, float]) -> Dict[str, float]:
        """清洗情绪值"""
        sanitized = {}
        
        for key, value in emotion.items():
            sanitized[key] = max(0, min(1, value))
        
        return sanitized


if __name__ == "__main__":
    validator = EmotionValidator()
    print(validator.validate_pad({"pleasure": 0.5, "arousal": 0.6, "dominance": 0.7}))
