"""
决策情绪系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import random


@dataclass
class DecisionOption:
    """决策选项"""
    id: str
    name: str
    value: float
    risk: float
    emotional_value: float = 0.0


class AffectiveDecisionMaking:
    """情绪化决策"""
    
    def __init__(self):
        self.risk_tolerance = 0.5
        self.emotion_influence = 0.3
    
    def evaluate_options(
        self,
        options: List[DecisionOption],
        current_emotion: Dict[str, float]
    ) -> List[DecisionOption]:
        """评估选项"""
        # 情绪影响
        emotion_valence = current_emotion.get("pleasure", 0)
        
        for option in options:
            # 情绪调整价值
            emotional_adjustment = emotion_valence * self.emotion_influence * option.emotional_value
            
            # 风险调整
            risk_adjustment = (0.5 - self.risk_tolerance) * option.risk * 0.2
            
            option.value += emotional_adjustment - risk_adjustment
        
        return sorted(options, key=lambda o: o.value, reverse=True)
    
    def select(
        self,
        options: List[DecisionOption],
        current_emotion: Dict[str, float]
    ) -> Optional[DecisionOption]:
        """选择最佳选项"""
        evaluated = self.evaluate_options(options, current_emotion)
        return evaluated[0] if evaluated else None


class RiskAssessment:
    """风险评估"""
    
    def __init__(self):
        self.risk_memory = {}
    
    def assess(
        self,
        option: DecisionOption,
        context: Dict
    ) -> float:
        """评估风险"""
        base_risk = option.risk
        
        # 记忆调整
        memory_risk = self.risk_memory.get(option.id, 0)
        
        # 环境调整
        stress = context.get("stress_level", 0.5)
        
        # 高压力增加感知风险
        if stress > 0.7:
            base_risk *= 1.3
        
        return min(1.0, base_risk + memory_risk * 0.2)
    
    def learn_from_outcome(
        self,
        option_id: str,
        outcome_value: float
    ):
        """从结果学习"""
        if option_id not in self.risk_memory:
            self.risk_memory[option_id] = 0.5
        
        # 负面结果增加风险感知
        if outcome_value < 0:
            self.risk_memory[option_id] = min(1.0, self.risk_memory[option_id] + 0.1)


if __name__ == "__main__":
    options = [
        DecisionOption("1", "Option A", 0.8, 0.3),
        DecisionOption("2", "Option B", 0.6, 0.6),
    ]
    
    dm = AffectiveDecisionMaking()
    selected = dm.select(options, {"pleasure": 0.5})
    print(f"Selected: {selected.name if selected else 'None'}")
