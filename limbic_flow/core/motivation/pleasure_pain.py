"""
愉悦-疼痛系统 - 基于研究文档实现

参考:
- PLEASURE_PAIN_SYSTEMS.md
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum
import math
import random


class PainType(Enum):
    """疼痛类型"""
    ACUTE = "acute"           # 急性疼痛
    CHRONIC = "chronic"       # 慢性疼痛
    EMOTIONAL = "emotional"  # 情感疼痛


class PleasureType(Enum):
    """愉悦类型"""
    HEDONIC = "hedonic"       # 感官愉悦
    EUDAIMONIC = "eudaimonic" # 意义满足
    ANTICIPATORY = "anticipatory"  # 预期愉悦
    REWARD_LEARNING = "reward_learning"  # 奖励学习


@dataclass
class PainSignal:
    """疼痛信号"""
    pain_type: PainType
    intensity: float        # 强度 [0-1]
    location: str          # 位置
    quality: str           # 性质 (锐痛/钝痛)
    threshold: float = 0.3  # 触发阈值
    adaptation: float = 0.0 # 适应因子


@dataclass
class PleasureSignal:
    """愉悦信号"""
    pleasure_type: PleasureType
    intensity: float        # 强度 [0-1]
    hedonic_value: float   # 内在愉悦值 [-1, 1]
    surprise_factor: float = 0.0  # 惊喜因子


class PainSystem:
    """
    疼痛系统
    
    研究: 
    - 伤害感受 (nociception)
    - 疼痛维度 (感觉-情感-认知)
    - 门控理论
    """
    
    def __init__(self):
        self.current_pain: Optional[PainSignal] = None
        self.pain_history: list = []
        
        # 参数
        self.threshold = 0.3
        self.adaptation_rate = 0.1
        self.saturation_point = 0.9
    
    def process_stimulus(
        self,
        stimulus_type: str,
        intensity: float,
        location: str = "unknown"
    ) -> PainSignal:
        """
        处理刺激
        
        Args:
            stimulus_type: 刺激类型 (thermal/mechanical/chemical/emotional)
            intensity: 强度 [0-1]
            location: 位置
        
        Returns:
            PainSignal: 疼痛信号
        """
        # 计算疼痛强度
        pain_intensity = self._calculate_pain_intensity(
            stimulus_type, intensity
        )
        
        # 检查是否超过阈值
        if pain_intensity < self.threshold:
            return PainSignal(
                pain_type=PainType.ACUTE,
                intensity=0.0,
                location=location,
                quality="none"
            )
        
        # 疼痛类型
        if intensity > 0.7:
            pain_type = PainType.ACUTE
            quality = "sharp"
        else:
            pain_type = PainType.CHRONIC
            quality = "aching"
        
        # 适应因子
        adaptation = self._calculate_adaptation(stimulus_type)
        
        signal = PainSignal(
            pain_type=pain_type,
            intensity=pain_intensity * (1 - adaptation),
            location=location,
            quality=quality,
            threshold=self.threshold,
            adaptation=adaptation
        )
        
        self.current_pain = signal
        self.pain_history.append(signal)
        
        return signal
    
    def _calculate_pain_intensity(
        self, 
        stimulus_type: str, 
        intensity: float
    ) -> float:
        """计算疼痛强度"""
        # 不同类型刺激的权重
        weights = {
            "thermal": 1.0,
            "mechanical": 0.9,
            "chemical": 0.85,
            "emotional": 0.7,
            "social": 0.6
        }
        
        weight = weights.get(stimulus_type, 0.5)
        
        # 饱和效应
        intensity = min(intensity, self.saturation_point)
        
        return intensity * weight
    
    def _calculate_adaptation(self, stimulus_type: str) -> float:
        """计算适应因子"""
        # 重复刺激导致适应
        recent_stimuli = [
            s for s in self.pain_history[-5:]
            if s.location == stimulus_type
        ]
        
        if len(recent_stimuli) > 2:
            return min(0.5, len(recent_stimuli) * self.adaptation_rate)
        
        return 0.0
    
    def get_avoidance_signal(self) -> float:
        """获取回避信号"""
        if not self.current_pain:
            return 0.0
        
        # 疼痛驱动回避行为
        return self.current_pain.intensity * 0.8
    
    def apply_gate_control(self, attention_level: float) -> float:
        """
        门控机制
        
        研究: 注意力可以调节疼痛感知
        """
        if not self.current_pain:
            return 0.0
        
        # 高注意力 = 更强疼痛感知
        # 低注意力 = 门关闭,减少疼痛
        gate_factor = attention_level
        
        return self.current_pain.intensity * gate_factor


class PleasureSystem:
    """
    愉悦系统
    
    研究:
    - 中脑边缘多巴胺通路
    - 愉悦类型
    - 奖励预测误差
    """
    
    def __init__(self):
        self.current_pleasure: Optional[PleasureSignal] = None
        self.satiety_level = 0.0  # 饱足度
        self.baseline_pleasure = 0.3  # 基础愉悦
        
        # 参数
        self.satiety_decay = 0.1
        self.anticipation_boost = 0.2
    
    def process_reward(
        self,
        reward_type: str,
        value: float,
        expected: bool = False
    ) -> PleasureSignal:
        """
        处理奖励
        
        Args:
            reward_type: 奖励类型
            value: 奖励值
            expected: 是否预期内
        """
        # 计算惊喜因子
        if expected:
            surprise_factor = 0.0
        else:
            surprise_factor = value * 0.5
        
        # 愉悦类型
        if "food" in reward_type or "sensory" in reward_type:
            pleasure_type = PleasureType.HEDONIC
        elif "meaning" in reward_type or "accomplish" in reward_type:
            pleasure_type = PleasureType.EUDAIMONIC
        elif "expect" in reward_type:
            pleasure_type = PleasureType.ANTICIPATORY
        else:
            pleasure_type = PleasureType.REWARD_LEARNING
        
        # 计算愉悦强度
        hedonic_value = value * 2 - 1  # 转换到 [-1, 1]
        
        intensity = (
            abs(hedonic_value) * 
            (1 + surprise_factor) * 
            (1 - self.satiety_level)
        )
        
        signal = PleasureSignal(
            pleasure_type=pleasure_type,
            intensity=min(1.0, intensity),
            hedonic_value=hedonic_value,
            surprise_factor=surprise_factor
        )
        
        self.current_pleasure = signal
        
        # 更新饱足度
        if value > 0:
            self.satiety_level = min(1.0, self.satiety_level + value * 0.2)
        
        return signal
    
    def get_approach_signal(self) -> float:
        """获取趋近信号"""
        if not self.current_pleasure:
            return 0.0
        
        # 正愉悦驱动趋近行为
        return self.current_pleasure.intensity if self.current_pleasure.hedonic_value > 0 else 0.0
    
    def decay_satiety(self):
        """饱足度衰减"""
        self.satiety_level = max(0, self.satiety_level - self.satiety_decay)
    
    def get_anticipatory_pleasure(self, expected_value: float) -> float:
        """获取预期愉悦"""
        # 预期奖励也产生愉悦
        return expected_value * (1 + self.anticipation_boost)


class OpponentProcessModel:
    """
    对手过程模型
    
    研究:
    - 愉悦和疼痛作为对手过程
    - 适应和调节
    """
    
    def __init__(self):
        self.pleasure_system = PleasureSystem()
        self.pain_system = PainSystem()
        
        # 状态
        self.pleasure_level = 0.0
        self.pain_level = 0.0
        
        # 参数
        self.opponent_strength = 0.5
        self.balance_point = 0.0
    
    def process(
        self,
        stimulus: Dict
    ) -> Dict:
        """
        处理刺激
        
        Args:
            stimulus: 包含 type 和 intensity
        """
        stimulus_type = stimulus.get("type", "neutral")
        intensity = stimulus.get("intensity", 0.0)
        
        if intensity <= 0:
            # 中性刺激
            self._decay_levels()
            
            return self._get_state()
        
        # 判断是愉悦还是疼痛刺激
        if stimulus_type in ["reward", "pleasure", "food", "social"]:
            signal = self.pleasure_system.process_reward(
                stimulus_type, intensity,
                stimulus.get("expected", False)
            )
            self.pleasure_level = signal.intensity
            
            # 对手过程: 愉悦后疼痛增加
            self.pain_level = self.pleasure_level * self.opponent_strength * 0.2
            
        elif stimulus_type in ["threat", "pain", "loss", "social_loss"]:
            signal = self.pain_system.process_stimulus(
                stimulus_type, intensity
            )
            self.pain_level = signal.intensity
            
            # 对手过程: 疼痛后愉悦增加
            self.pleasure_level = self.pain_level * self.opponent_strength * 0.2
        
        # 平衡
        self._balance()
        
        return self._get_state()
    
    def _decay_levels(self):
        """衰减到基线"""
        decay_rate = 0.05
        
        self.pleasure_level = max(self.baseline_pleasure, 
                                   self.pleasure_level - decay_rate)
        self.pain_level = max(0, self.pain_level - decay_rate)
    
    def _balance(self):
        """平衡愉悦和疼痛"""
        # 净状态
        net = self.pleasure_level - self.pain_level
        
        # 趋向平衡点
        self.pleasure_level = max(0, net + self.balance_point)
        self.pain_level = max(0, -net + self.balance_point)
    
    def _get_state(self) -> Dict:
        """获取当前状态"""
        return {
            "pleasure_level": self.pleasure_level,
            "pain_level": self.pain_level,
            "net_state": self.pleasure_level - self.pain_level,
            "is_pleasant": self.pleasure_level > self.pain_level,
            "approach_signal": self.pleasure_system.get_approach_signal(),
            "avoidance_signal": self.pain_system.get_avoidance_signal()
        }


# 示例
if __name__ == "__main__":
    # 测试对手过程模型
    model = OpponentProcessModel()
    
    # 奖励刺激
    result = model.process({
        "type": "reward",
        "intensity": 0.8,
        "expected": False
    })
    
    print(f"After reward: {result}")
    
    # 疼痛刺激
    result = model.process({
        "type": "threat",
        "intensity": 0.6
    })
    
    print(f"After threat: {result}")
