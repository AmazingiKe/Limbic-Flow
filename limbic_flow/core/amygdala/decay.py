"""
情绪衰减计算器 - 模拟情绪随时间的自然衰减

这是系统的"时间"组件:
- 情绪不会永远持续，会随时间自然衰减
- 不同的情绪有不同的衰减速度
- 类似于放射性衰变，使用半衰期模型
"""

import math
from dataclasses import dataclass
from typing import Dict, Any
from limbic_flow.core.config import HalfLifeConfig, BaselineConfig


@dataclass
class EmotionalState:
    """
    情绪状态 - 核心数据模型
    
    使用更清晰的数据结构，便于在系统各部分之间传递
    """
    pleasure: float = 0.0      # 愉悦度 [-1, 1]
    arousal: float = 0.0       # 唤醒度 [-1, 1]
    dominance: float = 0.0    # 控制度 [-1, 1]
    dopamine: float = 0.5      # 多巴胺 [0, 1]
    cortisol: float = 0.3      # 皮质醇 [0, 1]
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "pleasure": self.pleasure,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "dopamine": self.dopamine,
            "cortisol": self.cortisol,
        }
    
    @staticmethod
    def from_dict(d: Dict[str, float]) -> "EmotionalState":
        return EmotionalState(
            pleasure=d.get("pleasure", 0.0),
            arousal=d.get("arousal", 0.0),
            dominance=d.get("dominance", 0.0),
            dopamine=d.get("dopamine", 0.5),
            cortisol=d.get("cortisol", 0.3),
        )


class DecayCalculator:
    """
    衰减计算器 - 负责计算情绪随时间的衰减
    
    使用半衰期模型:
    - 半衰期越长，衰减越慢（情绪持续更久）
    - 半衰期越短，衰减越快（情绪来得快去得也快）
    
    设计原则:
    - 纯函数式计算，便于测试
    - 不存储状态，只做计算
    - 可以配置不同的半衰期参数
    """
    
    def __init__(self, config: HalfLifeConfig = None):
        self.config = config or HalfLifeConfig()
    
    def calculate_decay_factor(self, time_delta: float, half_life: float) -> float:
        """
        计算给定时间差对应的衰减因子
        
        公式: decay = e^(-ln(2) * Δt / T)
        
        Args:
            time_delta: 经过的时间（秒）
            half_life: 半衰期（秒）
        
        Returns:
            衰减因子 [0, 1]
        """
        if time_delta <= 0 or half_life <= 0:
            return 1.0
        return math.exp(-math.log(2) * time_delta / half_life)
    
    def decay_state(
        self, 
        state: EmotionalState, 
        time_delta: float,
        baseline: BaselineConfig = None
    ) -> EmotionalState:
        """
        对情绪状态应用时间衰减
        
        情绪会随时间逐渐回归到基线（默认为中性0）
        神经递质会回归到默认水平
        
        Args:
            state: 当前情绪状态
            time_delta: 经过的时间（秒）
            baseline: 基线配置
        
        Returns:
            衰减后的新状态
        """
        baseline = baseline or BaselineConfig()
        
        # 计算各维度的衰减因子
        decay_p = self.calculate_decay_factor(time_delta, self.config.pleasure)
        decay_a = self.calculate_decay_factor(time_delta, self.config.arousal)
        decay_d = self.calculate_decay_factor(time_delta, self.config.dominance)
        decay_dop = self.calculate_decay_factor(time_delta, self.config.dopamine)
        decay_cort = self.calculate_decay_factor(time_delta, self.config.cortisol)
        
        # PAD 向量衰减到基线
        new_pleasure = state.pleasure * decay_p
        new_arousal = state.arousal * decay_a
        new_dominance = state.dominance * decay_d
        
        # 神经递质回归到基线
        new_dopamine = baseline.dopamine + (state.dopamine - baseline.dopamine) * decay_dop
        new_cortisol = baseline.cortisol + (state.cortisol - baseline.cortisol) * decay_cort
        
        return EmotionalState(
            pleasure=new_pleasure,
            arousal=new_arousal,
            dominance=new_dominance,
            dopamine=max(0.0, min(1.0, new_dopamine)),
            cortisol=max(0.0, min(1.0, new_cortisol)),
        )
    
    def apply_stimulus(
        self, 
        state: EmotionalState, 
        pleasure_delta: float = 0.0,
        arousal_delta: float = 0.0,
        dominance_delta: float = 0.0
    ) -> EmotionalState:
        """
        应用情绪刺激
        
        在当前状态基础上叠加新的刺激
        
        Args:
            state: 当前情绪状态
            pleasure_delta: 愉悦度变化 [-1, 1]
            arousal_delta: 唤醒度变化 [-1, 1]
            dominance_delta: 控制度变化 [-1, 1]
        
        Returns:
            应用刺激后的新状态
        """
        new_pleasure = state.pleasure + pleasure_delta
        new_arousal = state.arousal + arousal_delta
        new_dominance = state.dominance + dominance_delta
        
        return EmotionalState(
            pleasure=max(-1.0, min(1.0, new_pleasure)),
            arousal=max(-1.0, min(1.0, new_arousal)),
            dominance=max(-1.0, min(1.0, new_dominance)),
            dopamine=state.dopamine,
            cortisol=state.cortisol,
        )
    
    def update_neurotransmitters(
        self, 
        state: EmotionalState
    ) -> EmotionalState:
        """
        根据当前情绪状态更新神经递质
        
        情绪状态会影响神经递质的释放:
        - 愉悦感增加多巴胺
        - 唤醒度高增加皮质醇
        
        Args:
            state: 当前情绪状态
        
        Returns:
            更新神经递质后的状态
        """
        # 愉悦度影响多巴胺
        dopamine_change = state.pleasure * 0.1
        new_dopamine = state.dopamine + dopamine_change
        
        # 唤醒度影响皮质醇
        cortisol_change = abs(state.arousal) * 0.1
        new_cortisol = state.cortisol + cortisol_change
        
        return EmotionalState(
            pleasure=state.pleasure,
            arousal=state.arousal,
            dominance=state.dominance,
            dopamine=max(0.0, min(1.0, new_dopamine)),
            cortisol=max(0.0, min(1.0, new_cortisol)),
        )


# 便捷函数 - 使用默认配置创建计算器
_default_calculator = None

def get_default_calculator() -> DecayCalculator:
    """获取默认的衰减计算器"""
    global _default_calculator
    if _default_calculator is None:
        _default_calculator = DecayCalculator()
    return _default_calculator
