"""
压力响应系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict
import math
import time


@dataclass
class StressResponse:
    """压力响应"""
    cortisol_level: float
    heart_rate: float
    cognitive_impact: float


class StressSystem:
    """压力系统 (HPA轴)"""
    
    def __init__(self):
        self.baseline_cortisol = 0.2
        self.current_cortisol = 0.2
        self.stress_threshold = 0.6
        self.recovery_rate = 0.02
    
    def acute_stress(self, intensity: float) -> StressResponse:
        """急性压力响应"""
        # 皮质醇上升
        self.current_cortisol = min(1.0, self.baseline_cortisol + intensity * 0.6)
        
        # 心率增加
        heart_rate = 70 + intensity * 40
        
        # 认知影响
        if intensity > 0.7:
            cognitive_impact = -0.3  # 决策受损
        elif intensity > 0.4:
            cognitive_impact = -0.1  # 轻微影响
        else:
            cognitive_impact = 0.1   # 轻微增强
        
        return StressResponse(
            cortisol_level=self.current_cortisol,
            heart_rate=heart_rate,
            cognitive_impact=cognitive_impact
        )
    
    def chronic_stress(self, duration_hours: float) -> float:
        """慢性压力 (累积)"""
        # 长期压力导致皮质醇持续升高
        cumulative = duration_hours * 0.01
        return min(1.0, self.baseline_cortisol + cumulative)
    
    def recover(self):
        """恢复"""
        self.current_cortisol = max(
            self.baseline_cortisol,
            self.current_cortisol - self.recovery_rate
        )
    
    def get_allostatic_load(self, stress_history: list) -> float:
        """计算allo静态负荷 (累积压力)"""
        if not stress_history:
            return 0.0
        
        # 加权平均
        total = sum(s * w for s, w in zip(stress_history[-10:], 
                                           [0.5, 0.3, 0.2][:len(stress_history[-10:])]))
        return total


class StressRecovery:
    """压力恢复"""
    
    def __init__(self):
        self.social_support = 0.5
        self.coping_strategies = []
    
    def get_recovery_time(
        self,
        stress_intensity: float,
        has_support: bool = True
    ) -> float:
        """恢复时间 (分钟)"""
        base_time = stress_intensity * 60
        
        # 社会支持减少恢复时间
        if has_support:
            base_time *= 0.7
        
        return base_time
    
    def calculate_resilience(self) -> float:
        """计算韧性"""
        resilience = 0.5 + self.social_support * 0.3
        
        if len(self.coping_strategies) > 3:
            resilience += 0.2
        
        return min(1.0, resilience)


if __name__ == "__main__":
    stress = StressSystem()
    response = stress.acute_stress(0.8)
    print(f"Cortisol: {response.cortisol_level:.2f}")
