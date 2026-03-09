"""
人格建模系统 - 基于研究文档实现
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


class TraitType(Enum):
    """大五人格特质"""
    OPENNESS = "openness"           # 开放性
    CONSCIENTIOUSNESS = "conscientiousness"  # 尽责性
    EXTRAVERSION = "extraversion"   # 外向性
    AGREEABLENESS = "agreeableness"  # 宜人性
    NEUROTICISM = "neuroticism"    # 神经质


@dataclass
class PersonalityProfile:
    """人格配置"""
    traits: Dict[TraitType, float] = field(default_factory=dict)
    stable_traits: Dict[str, float] = field(default_factory=dict)  # 固定特质


class BigFivePersonality:
    """大五人格模型"""
    
    def __init__(self):
        self.profile = PersonalityProfile()
        self._init_traits()
    
    def _init_traits(self):
        """初始化特质"""
        for trait in TraitType:
            self.profile.traits[trait] = 0.5
    
    def set_trait(self, trait: TraitType, value: float):
        self.profile.traits[trait] = max(0, min(1, value))
    
    def get_trait(self, trait: TraitType) -> float:
        return self.profile.traits.get(trait, 0.5)
    
    def get_emotion_bias(self) -> Dict[str, float]:
        """获取情绪偏见"""
        neuroticism = self.get_trait(TraitType.NEUROTICISM)
        extraversion = self.get_trait(TraitType.EXTRAVERSION)
        
        return {
            "negativity_bias": neuroticism * 0.5,
            "positivity_bias": extraversion * 0.3,
            "arousal_tendency": (1 - neuroticism) * 0.2
        }


class PersonalityEmotionLink:
    """人格-情绪链接"""
    
    def __init__(self, personality: BigFivePersonality):
        self.personality = personality
    
    def get_regulation_tendency(self) -> str:
        """获取调节倾向"""
        if self.personality.get_trait(TraitType.NEUROTICISM) > 0.6:
            return "avoidance"
        elif self.personality.get_trait(TraitType.CONSCIENTIOUSNESS) > 0.6:
            return "problem_focused"
        else:
            return "emotional_expression"
    
    def get_response_style(self) -> str:
        """获取反应风格"""
        agree = self.personality.get_trait(TraitType.AGREEABLENESS)
        if agree > 0.7:
            return "accommodating"
        elif agree < 0.3:
            return "competitive"
        else:
            return "collaborative"


class PersonalityEvolution:
    """人格演变"""
    
    def __init__(self):
        self.change_rate = 0.01
    
    def evolve(
        self,
        personality: BigFivePersonality,
        experiences: List[Dict],
        years: float
    ):
        """随经验演变"""
        for exp in experiences:
            impact = exp.get("impact", 0.1)
            affected_trait = exp.get("trait")
            
            if affected_trait:
                change = impact * self.change_rate * years
                personality.set_trait(affected_trait, 
                    personality.get_trait(affected_trait) + change)


if __name__ == "__main__":
    p = BigFivePersonality()
    p.set_trait(TraitType.EXTRAVERSION, 0.8)
    print(p.get_emotion_bias())
