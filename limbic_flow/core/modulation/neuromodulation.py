"""
神经调控模拟系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict
import math


@dataclass
class NeuromodulationState:
    """神经调控状态"""
    acetylcholine: float = 0.5  # 注意力
    norepinephrine: float = 0.5  # 唤醒
    dopamine: float = 0.5       # 奖励
    serotonin: float = 0.5      # 情绪稳定


class NeuromodulationSystem:
    """神经调控系统"""
    
    def __init__(self):
        self.state = NeuromodulationState()
    
    def update_attention(self, task_demand: float):
        """更新注意力 (乙酰胆碱)"""
        # 高任务需求 -> 高乙酰胆碱
        self.state.acetylcholine = min(1.0, 0.3 + task_demand * 0.7)
    
    def update_arousal(self, novelty: float):
        """更新唤醒 (去甲肾上腺素)"""
        self.state.norepinephrine = min(1.0, 0.3 + novelty * 0.7)
    
    def update_reward(self, reward: float):
        """更新奖励 (多巴胺)"""
        self.state.dopamine = min(1.0, 0.3 + reward * 0.7)
    
    def update_mood(self, stress: float):
        """更新情绪 (血清素)"""
        # 压力降低血清素
        self.state.serotonin = max(0.1, 0.6 - stress * 0.5)
    
    def get_attention_weight(self) -> float:
        """获取注意力权重"""
        return self.state.acetylcholine
    
    def get_arousal_level(self) -> float:
        """获取唤醒水平"""
        return self.state.norepinephrine
    
    def get_motivation(self) -> float:
        """获取动机水平"""
        return (self.state.dopamine + self.state.norepinephrine) / 2


if __name__ == "__main__":
    nm = NeuromodulationSystem()
    nm.update_attention(0.8)
    nm.update_reward(0.6)
    print(f"Attention: {nm.get_attention_weight()}")
