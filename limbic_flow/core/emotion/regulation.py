"""
情绪调节算法模块

参考:
- EMOTION_REGULATION_ALGORITHMS.md
- STRESS_RESPONSE_SYSTEMS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import math
import random


class RegulationStrategy(Enum):
    """情绪调节策略"""
    NONE = "none"                          # 无调节
    COGNITIVE_REAPPRAISAL = "reappraisal"  # 认知重评
    SUPPRESSION = "suppression"            # 情绪抑制
    EXPRESSION = "expression"              # 情绪表达
    MINDFULNESS = "mindfulness"           # 正念
    DISTRESS_TOLERANCE = "distress_tolerance"  # 痛苦耐受
    ACCEPTANCE = "acceptance"              # 接纳
    PROBLEM_FOCUSED = "problem_focused"   # 问题聚焦
    DISTANCE = "distance"                  # 心理距离


@dataclass
class RegulationResult:
    """调节结果"""
    strategy: RegulationStrategy
    original_pad: Dict[str, float]
    regulated_pad: Dict[str, float]
    confidence: float = 0.8
    description: str = ""


class CognitiveReappraisal:
    """
    认知重评 (Cognitive Reappraisal)
    
    研究参考:
    - Gross's process model of emotion regulation
    - 改变对事件的解释来改变情绪反应
    
    策略:
    - 重新解释情境意义
    - 关注积极面
    - 情境重构
    - 向下比较
    """
    
    def __init__(self):
        self.reappraisal_operators = {
            "reframe": self._reframe,
            "positive_refocus": self._positive_refocus,
            "contextualize": self._contextualize,
            "downward_compare": self._downward_compare,
            "meaning_finding": self._meaning_finding,
        }
    
    def apply(
        self, 
        pad: Dict[str, float], 
        context: str,
        strategy: str = "reframe"
    ) -> RegulationResult:
        """
        应用认知重评
        
        Args:
            pad: 当前PAD状态
            context: 情境描述
            strategy: 重评策略
        
        Returns:
            RegulationResult: 调节结果
        """
        original = pad.copy()
        
        if strategy in self.reappraisal_operators:
            regulated = self.reappraisal_operators[strategy](pad, context)
        else:
            regulated = pad.copy()
        
        return RegulationResult(
            strategy=RegulationStrategy.COGNITIVE_REAPPRAISAL,
            original_pad=original,
            regulated_pad=regulated,
            description=f"Applied {strategy} reappraisal"
        )
    
    def _reframe(self, pad: Dict[str, float], context: str) -> Dict[str, float]:
        """重新框架 - 改变对事件的理解"""
        # 降低负面情绪，增加掌控感
        result = pad.copy()
        
        # 如果是负面情绪，尝试转化为中性或积极
        if result["pleasure"] < 0:
            # 增加愉悦度
            result["pleasure"] = min(0.5, result["pleasure"] + 0.3)
            # 增加掌控感
            result["dominance"] = min(1.0, result["dominance"] + 0.2)
        
        return result
    
    def _positive_refocus(self, pad: Dict[str, float], context: str) -> Dict[str, float]:
        """积极重定向 - 关注积极面"""
        result = pad.copy()
        
        # 提升愉悦度
        result["pleasure"] = min(1.0, result["pleasure"] + 0.25)
        # 降低唤醒度（平静下来）
        result["arousal"] = max(0.0, result["arousal"] - 0.15)
        
        return result
    
    def _contextualize(self, pad: Dict[str, float], context: str) -> Dict[str, float]:
        """情境化 - 从更宽的视角看问题"""
        result = pad.copy()
        
        # 增加掌控感（理解情境）
        result["dominance"] = min(1.0, result["dominance"] + 0.2)
        # 降低唤醒度（平静）
        result["arousal"] = max(0.0, result["arousal"] - 0.1)
        
        return result
    
    def _downward_compare(self, pad: Dict[str, float], context: str) -> Dict[str, float]:
        """向下比较 - 比上不足比下有余"""
        result = pad.copy()
        
        # 提升愉悦度
        result["pleasure"] = min(1.0, result["pleasure"] + 0.2)
        
        return result
    
    def _meaning_finding(self, pad: Dict[str, float], context: str) -> Dict[str, float]:
        """寻找意义 - 从困难中找成长"""
        result = pad.copy()
        
        # 提升愉悦度
        result["pleasure"] = min(1.0, result["pleasure"] + 0.15)
        # 增加掌控感
        result["dominance"] = min(1.0, result["dominance"] + 0.15)
        
        return result


class EmotionSuppression:
    """
    情绪抑制 (Emotion Suppression)
    
    研究参考:
    - Gross's response-focused strategy
    - 抑制情绪表达但可能增加生理激活
    - 短期有效但长期有成本
    """
    
    def __init__(self):
        self.cognitive_cost = 0.15  # 抑制的认知成本
    
    def apply(self, pad: Dict[str, float]) -> RegulationResult:
        """
        应用情绪抑制
        
        降低外在表达但可能增加内在激活
        """
        original = pad.copy()
        result = pad.copy()
        
        # 降低唤醒度（外在表现平静）
        result["arousal"] = result["arousal"] * 0.7
        
        # 降低愉悦度表达（但内心可能更强烈）
        # 长期来看会消耗认知资源
        
        return RegulationResult(
            strategy=RegulationStrategy.SUPPRESSION,
            original_pad=original,
            regulated_pad=result,
            confidence=0.6,  # 抑制效果不稳定
            description="Suppressed emotional expression"
        )


class MindfulnessRegulation:
    """
    正念调节 (Mindfulness-based Regulation)
    
    研究参考:
    - 去中心化 (Decentering)
    - 专注当下
    - 非反应性观察
    """
    
    def apply(self, pad: Dict[str, float], context: str = "") -> RegulationResult:
        """
        应用正念调节
        
        - 降低情绪反应性
        - 增加情绪觉察
        - 不评判地观察情绪
        """
        original = pad.copy()
        result = pad.copy()
        
        # 降低唤醒度（平静下来）
        result["arousal"] = max(0.0, result["arousal"] - 0.3)
        
        # 增加掌控感（觉察带来掌控）
        result["dominance"] = min(1.0, result["dominance"] + 0.15)
        
        # 调整愉悦度趋向中性
        if abs(result["pleasure"]) > 0.3:
            result["pleasure"] = result["pleasure"] * 0.8
        
        return RegulationResult(
            strategy=RegulationStrategy.MINDFULNESS,
            original_pad=original,
            regulated_pad=result,
            confidence=0.85,
            description="Applied mindfulness regulation"
        )


class DistressTolerance:
    """
    痛苦耐受技能 (Distress Tolerance)
    
    研究参考:
    - DBT (Dialectical Behavior Therapy)
    - TIPP 技术: 温度、运动、剧烈运动、放松呼吸
    """
    
    def __init__(self):
        self.techniques = {
            "tip": self._tip,
            "self_soothe": self._self_soothe,
            "radical_acceptance": self._radical_acceptance,
            " IMPROVE": self._improve,
        }
    
    def apply(self, pad: Dict[str, float], technique: str = "tip") -> RegulationResult:
        """应用痛苦耐受技术"""
        original = pad.copy()
        
        if technique in self.techniques:
            result = self.techniques[technique](pad)
        else:
            result = pad.copy()
        
        return RegulationResult(
            strategy=RegulationStrategy.DISTRESS_TOLERANCE,
            original_pad=original,
            regulated_pad=result,
            description=f"Applied {technique} technique"
        )
    
    def _tip(self, pad: Dict[str, float]) -> Dict[str, float]:
        """TIPP: 温度、运动、剧烈运动、放松"""
        result = pad.copy()
        
        # 剧烈运动降低唤醒
        result["arousal"] = max(0.0, result["arousal"] - 0.4)
        # 增加掌控感
        result["dominance"] = min(1.0, result["dominance"] + 0.2)
        
        return result
    
    def _self_soothe(self, pad: Dict[str, float]) -> Dict[str, float]:
        """自我安抚"""
        result = pad.copy()
        
        # 提升愉悦度
        result["pleasure"] = min(1.0, result["pleasure"] + 0.2)
        # 降低唤醒度
        result["arousal"] = max(0.0, result["arousal"] - 0.2)
        
        return result
    
    def _radical_acceptance(self, pad: Dict[str, float]) -> Dict[str, float]:
        """完全接纳"""
        result = pad.copy()
        
        # 增加掌控感（接纳带来掌控）
        result["dominance"] = min(1.0, result["dominance"] + 0.25)
        # 降低情绪波动
        result["arousal"] = result["arousal"] * 0.7
        
        return result
    
    def _improve(self, pad: Dict[str, float]) -> Dict[str, float]:
        """IMPROVE: 想象、意义、放松、正念、回忆、警醒"""
        result = pad.copy()
        
        # 降低唤醒
        result["arousal"] = max(0.0, result["arousal"] - 0.25)
        # 增加掌控
        result["dominance"] = min(1.0, result["dominance"] + 0.15)
        
        return result


class EmotionRegulationEngine:
    """
    情绪调节引擎
    
    整合多种调节策略，根据上下文自动选择最佳策略
    """
    
    def __init__(self):
        self.reappraisal = CognitiveReappraisal()
        self.suppression = EmotionSuppression()
        self.mindfulness = MindfulnessRegulation()
        self.distress_tolerance = DistressTolerance()
        
        # 策略选择规则
        self.strategy_rules = {
            "high_arousal": self._handle_high_arousal,
            "low_dominance": self._handle_low_dominance,
            "negative_pleasure": self._handle_negative_pleasure,
            "high_stress": self._handle_high_stress,
        }
    
    def regulate(
        self,
        pad: Dict[str, float],
        context: str = "",
        forced_strategy: Optional[RegulationStrategy] = None
    ) -> RegulationResult:
        """
        调节情绪
        
        Args:
            pad: 当前PAD状态
            context: 情境上下文
            forced_strategy: 强制使用某策略
        
        Returns:
            RegulationResult: 调节结果
        """
        # 如果指定了策略，使用指定策略
        if forced_strategy:
            return self._apply_strategy(pad, context, forced_strategy)
        
        # 自动选择策略
        arousal = pad.get("arousal", 0.5)
        pleasure = pad.get("pleasure", 0.0)
        dominance = pad.get("dominance", 0.5)
        
        # 根据状态选择策略
        if arousal > 0.7:
            return self.strategy_rules["high_arousal"](pad, context)
        elif dominance < 0.3:
            return self.strategy_rules["low_dominance"](pad, context)
        elif pleasure < -0.3:
            return self.strategy_rules["negative_pleasure"](pad, context)
        else:
            # 默认使用正念
            return self.mindfulness.apply(pad, context)
    
    def _apply_strategy(
        self, 
        pad: Dict[str, float], 
        context: str,
        strategy: RegulationStrategy
    ) -> RegulationResult:
        """应用指定策略"""
        if strategy == RegulationStrategy.COGNITIVE_REAPPRAISAL:
            return self.reappraisal.apply(pad, context)
        elif strategy == RegulationStrategy.SUPPRESSION:
            return self.suppression.apply(pad)
        elif strategy == RegulationStrategy.MINDFULNESS:
            return self.mindfulness.apply(pad, context)
        elif strategy == RegulationStrategy.DISTRESS_TOLERANCE:
            return self.distress_tolerance.apply(pad)
        else:
            return RegulationResult(
                strategy=strategy,
                original_pad=pad,
                regulated_pad=pad.copy()
            )
    
    def _handle_high_arousal(self, pad: Dict[str, float], context: str) -> RegulationResult:
        """处理高唤醒"""
        # 高唤醒时使用正念或痛苦耐受
        if random.random() > 0.5:
            return self.mindfulness.apply(pad, context)
        else:
            return self.distress_tolerance.apply(pad, "tip")
    
    def _handle_low_dominance(self, pad: Dict[str, float], context: str) -> RegulationResult:
        """处理低掌控感"""
        # 低掌控感使用认知重评
        return self.reappraisal.apply(pad, context, "reframe")
    
    def _handle_negative_pleasure(self, pad: Dict[str, float], context: str) -> RegulationResult:
        """处理负面情绪"""
        # 负面情绪使用积极重定向
        return self.reappraisal.apply(pad, context, "positive_refocus")
    
    def _handle_high_stress(self, pad: Dict[str, float], context: str) -> RegulationResult:
        """处理高压"""
        return self.distress_tolerance.apply(pad, "radical_acceptance")


# 示例
if __name__ == "__main__":
    engine = EmotionRegulationEngine()
    
    # 测试高唤醒
    test_pad = {"pleasure": -0.3, "arousal": 0.8, "dominance": 0.4}
    result = engine.regulate(test_pad, "压力情境")
    print(f"Original: {result.original_pad}")
    print(f"Regulated: {result.regulated_pad}")
    print(f"Strategy: {result.strategy.value}")
