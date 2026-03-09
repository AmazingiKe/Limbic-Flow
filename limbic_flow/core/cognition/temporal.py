"""
时间感知系统 - 基于研究文档实现

参考:
- EMBODIED_COGNITION.md (Temporal Perception部分)
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import time
import math


@dataclass
class TimeExperience:
    """时间体验"""
    perceived_duration: float  # 感知时长
    subjective_speed: float    # 主观速度
    dilation_factor: float     # 膨胀因子


class SubjectiveTimePerception:
    """
    主观时间感知
    
    研究:
    - 主观时间 vs 客观时间
    - 时间膨胀/收缩
    - 记忆与时间
    """
    
    def __init__(self):
        self.baseline_speed = 1.0
        self.memory_weight = 0.3
    
    def perceive_duration(
        self,
        objective_seconds: float,
        emotional_state: Dict,
        attention_level: float
    ) -> TimeExperience:
        """
        感知时长
        
        - 高唤醒情绪 -> 时间变慢
        - 高注意力 -> 时间变慢
        - 新奇体验 -> 时间变慢
        """
        # 情绪影响
        arousal = emotional_state.get("arousal", 0.5)
        emotion_valence = emotional_state.get("pleasure", 0.0)
        
        # 唤醒效应: 高唤醒 = 时间膨胀
        arousal_factor = 1.0 + arousal * 0.5
        
        # 注意力效应
        attention_factor = 1.0 + attention_level * 0.3
        
        # 新奇效应 (简化)
        novelty_factor = 1.0 + (1.0 - attention_level) * 0.2
        
        # 综合
        dilation = arousal_factor * attention_factor * novelty_factor
        
        perceived = objective_seconds * (1.0 / dilation)
        
        return TimeExperience(
            perceived_duration=perceived,
            subjective_speed=dilation,
            dilation_factor=dilation
        )


class TimeMemoryIntegration:
    """
    记忆与时间整合
    
    研究: 时间感知依赖记忆
    """
    
    def __init__(self):
        self.event_markers = []
    
    def add_event_marker(self, event: str, timestamp: float):
        """添加事件标记"""
        self.event_markers.append({"event": event, "time": timestamp})
    
    def estimate_time_since(
        self,
        event: str,
        current_time: float
    ) -> float:
        """估计事件后经过的时间"""
        for marker in reversed(self.event_markers):
            if marker["event"] == event:
                return current_time - marker["time"]
        
        return 0.0
    
    def generate_time_estimate(self, seconds: float) -> str:
        """生成时间估计描述"""
        if seconds < 60:
            return "刚刚"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}分钟前"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours}小时前"
        else:
            days = int(seconds / 86400)
            return f"{days}天前"


if __name__ == "__main__":
    perception = SubjectiveTimePerception()
    
    result = perception.perceive_duration(
        60.0,
        {"arousal": 0.8, "pleasure": 0.3},
        0.9
    )
    
    print(f"Perceived: {result.perceived_duration:.1f}s")
    print(f"Dilation: {result.dilation_factor:.2f}x")
