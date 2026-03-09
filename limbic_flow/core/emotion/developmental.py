"""
发展情绪AI - 基于研究文档实现

参考:
- DEVELOPMENTAL_EMOTIONAL_AI.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import math


class DevelopmentalStage(Enum):
    """发展阶段"""
    INFANCY = "infancy"           # 0-2岁
    EARLY_CHILDHOOD = "early_childhood"  # 2-5岁
    MIDDLE_CHILDHOOD = "middle_childhood"  # 6-11岁
    ADOLESCENCE = "adolescence"  # 12-18岁
    EMERGING_ADULTHOOD = "emerging_adulthood"  # 18-25岁
    ADULTHOOD = "adulthood"     # 25-65岁
    LATE_ADULTHOOD = "late_adulthood"  # 65+岁


class PsychosocialCrisis(Enum):
    """心理社会危机"""
    TRUST = "trust"             # 信任
    AUTONOMY = "autonomy"      # 自主性
    INITIATIVE = "initiative"  # 主动性
    INDUSTRY = "industry"       # 勤奋
    IDENTITY = "identity"       # 身份认同
    INTIMACY = "intimacy"      # 亲密
    GENERATIVITY = "generativity"  # 生产力
    INTEGRITY = "integrity"     # 自我整合


@dataclass
class DevelopmentalProfile:
    """发展配置文件"""
    stage: DevelopmentalStage
    age_years: float
    
    # 心理社会危机
    crisis: PsychosocialCrisis
    
    # 情绪能力
    emotion_vocabulary_size: int
    self_regulation_ability: float  # 0-1
    metacognitive_ability: float    # 0-1
    
    # 特定情绪
    has_self_conscious_emotions: bool  # 羞耻/自豪等
    has_complex_emotions: bool         # 嫉妒/共情等


class EmotionalMaturityModel:
    """
    情绪成熟度模型
    
    研究: Erikson心理社会发展阶段
    """
    
    def __init__(self):
        self.stage_configs = self._init_stages()
        self.current_stage = DevelopmentalStage.ADULTHOOD
        self.age = 25.0
    
    def _init_stages(self) -> Dict[DevelopmentalStage, DevelopmentalProfile]:
        """初始化各阶段配置"""
        return {
            DevelopmentalStage.INFANCY: DevelopmentalProfile(
                stage=DevelopmentalStage.INFANCY,
                age_years=1.0,
                crisis=PsychosocialCrisis.TRUST,
                emotion_vocabulary_size=10,
                self_regulation_ability=0.2,
                metacognitive_ability=0.1,
                has_self_conscious_emotions=False,
                has_complex_emotions=False
            ),
            DevelopmentalStage.EARLY_CHILDHOOD: DevelopmentalProfile(
                stage=DevelopmentalStage.EARLY_CHILDHOOD,
                age_years=3.5,
                crisis=PsychosocialCrisis.AUTONOMY,
                emotion_vocabulary_size=50,
                self_regulation_ability=0.4,
                metacognitive_ability=0.2,
                has_self_conscious_emotions=True,
                has_complex_emotions=False
            ),
            DevelopmentalStage.MIDDLE_CHILDHOOD: DevelopmentalProfile(
                stage=DevelopmentalStage.MIDDLE_CHILDHOOD,
                age_years=8.0,
                crisis=PsychosocialCrisis.INDUSTRY,
                emotion_vocabulary_size=150,
                self_regulation_ability=0.6,
                metacognitive_ability=0.4,
                has_self_conscious_emotions=True,
                has_complex_emotions=True
            ),
            DevelopmentalStage.ADOLESCENCE: DevelopmentalProfile(
                stage=DevelopmentalStage.ADOLESCENCE,
                age_years=15.0,
                crisis=PsychosocialCrisis.IDENTITY,
                emotion_vocabulary_size=300,
                self_regulation_ability=0.7,
                metacognitive_ability=0.6,
                has_self_conscious_emotions=True,
                has_complex_emotions=True
            ),
            DevelopmentalStage.EMERGING_ADULTHOOD: DevelopmentalProfile(
                stage=DevelopmentalStage.EMERGING_ADULTHOOD,
                age_years=22.0,
                crisis=PsychosocialCrisis.INTIMACY,
                emotion_vocabulary_size=400,
                self_regulation_ability=0.8,
                metacognitive_ability=0.7,
                has_self_conscious_emotions=True,
                has_complex_emotions=True
            ),
            DevelopmentalStage.ADULTHOOD: DevelopmentalProfile(
                stage=DevelopmentalStage.ADULTHOOD,
                age_years=40.0,
                crisis=PsychosocialCrisis.GENERATIVITY,
                emotion_vocabulary_size=500,
                self_regulation_ability=0.9,
                metacognitive_ability=0.8,
                has_self_conscious_emotions=True,
                has_complex_emotions=True
            ),
            DevelopmentalStage.LATE_ADULTHOOD: DevelopmentalProfile(
                stage=DevelopmentalStage.LATE_ADULTHOOD,
                age_years=70.0,
                crisis=PsychosocialCrisis.INTEGRITY,
                emotion_vocabulary_size=500,
                self_regulation_ability=0.95,
                metacognitive_ability=0.9,
                has_self_conscious_emotions=True,
                has_complex_emotions=True
            ),
        }
    
    def set_age(self, age: float):
        """设置年龄,自动确定阶段"""
        self.age = age
        
        if age < 2:
            self.current_stage = DevelopmentalStage.INFANCY
        elif age < 5:
            self.current_stage = DevelopmentalStage.EARLY_CHILDHOOD
        elif age < 12:
            self.current_stage = DevelopmentalStage.MIDDLE_CHILDHOOD
        elif age < 18:
            self.current_stage = DevelopmentalStage.ADOLESCENCE
        elif age < 25:
            self.current_stage = DevelopmentalStage.EMERGING_ADULTHOOD
        elif age < 65:
            self.current_stage = DevelopmentalStage.ADULTHOOD
        else:
            self.current_stage = DevelopmentalStage.LATE_ADULTHOOD
    
    def get_profile(self) -> DevelopmentalProfile:
        """获取当前发展配置"""
        return self.stage_configs[self.current_stage]
    
    def get_age_appropriate_response(
        self,
        emotion: str,
        base_response: Dict
    ) -> Dict:
        """
        获取年龄适当的响应
        
        根据发展阶段调整情绪响应
        """
        profile = self.get_profile()
        
        adjusted = base_response.copy()
        
        # 调整自我调节能力
        adjusted["self_regulation"] = profile.self_regulation_ability
        
        # 调整元认知能力
        adjusted["metacognition"] = profile.metacognitive_ability
        
        # 检查是否应该有复杂情绪
        if not profile.has_self_conscious_emotions:
            # 婴幼儿没有自我意识情绪
            self_emotions = ["pride", "shame", "guilt", "embarrassment"]
            if emotion in self_emotions:
                adjusted["intensity"] = 0
        
        return adjusted
    
    def get_regulation_strategy(self) -> List[str]:
        """获取适合年龄的调节策略"""
        profile = self.get_profile()
        
        strategies = []
        
        if profile.self_regulation_ability < 0.3:
            strategies = ["co_regulation", "comfort_seeking", "distraction"]
        elif profile.self_regulation_ability < 0.6:
            strategies = ["distraction", "self_soothing", "support_seeking"]
        elif profile.self_regulation_ability < 0.8:
            strategies = ["cognitive_reappraisal", "problem_focused", "support_seeking"]
        else:
            strategies = ["cognitive_reappraisal", "mindfulness", "acceptance", "metacognition"]
        
        return strategies
    
    def get_emotional_vocabulary(self) -> List[str]:
        """获取适合年龄的情绪词汇"""
        profile = self.get_profile()
        
        # 基础情绪 (所有阶段)
        base_emotions = ["joy", "distress", "surprise", "fear", "anger", "disgust"]
        
        if not profile.has_self_conscious_emotions:
            return base_emotions
        
        # 自我意识情绪
        self_conscious = ["pride", "shame", "guilt", "embarrassment", "envy"]
        
        if profile.has_complex_emotions:
            # 复杂情绪
            complex = ["jealousy", "empathy", "compassion", "nostalgia", "contempt", "admiration"]
            return base_emotions + self_conscious + complex
        
        return base_emotions + self_conscious


class AttachmentStyle:
    """
    依恋风格
    
    研究: 依恋形成影响情绪发展
    """
    
    # 依恋类型
    SECURE = "secure"
    ANXIOUS = "anxious_ambivalent"
    AVOIDANT = "avoidant"
    DISORGANIZED = "disorganized"
    
    def __init__(self):
        self.style = self.SECURE
        self.attachment_history: List[str] = []
    
    def determine_style(
        self,
        caregiver_responsiveness: float,
        caregiver_availability: float
    ) -> str:
        """
        确定依恋风格
        
        基于养育者响应性和可用性
        """
        if caregiver_responsiveness > 0.7 and caregiver_availability > 0.7:
            self.style = self.SECURE
        elif caregiver_responsiveness < 0.3:
            self.style = self.AVOIDANT
        elif caregiver_availability < 0.3:
            self.style = self.ANXIOUS
        else:
            self.style = self.DISORGANIZED
        
        self.attachment_history.append(self.style)
        
        return self.style
    
    def get_emotional_pattern(self) -> Dict:
        """获取情绪模式"""
        patterns = {
            self.SECURE: {
                "emotion_regulation": "healthy",
                "trust_level": "high",
                "relationship_approach": "balanced"
            },
            self.ANXIOUS: {
                "emotion_regulation": "variable",
                "trust_level": "low",
                "relationship_approach": "clingy"
            },
            self.AVOIDANT: {
                "emotion_regulation": "suppressed",
                "trust_level": "low",
                "relationship_approach": "distant"
            },
            self.DISORGANIZED: {
                "emotion_regulation": "inconsistent",
                "trust_level": "very_low",
                "relationship_approach": "conflicted"
            }
        }
        
        return patterns[self.style]


# 示例
if __name__ == "__main__":
    # 创建发展模型
    model = EmotionalMaturityModel()
    
    # 设置不同年龄
    ages = [2, 8, 15, 25, 70]
    
    for age in ages:
        model.set_age(age)
        profile = model.get_profile()
        
        print(f"\nAge: {age}, Stage: {profile.stage.value}")
        print(f"Crisis: {profile.crisis.value}")
        print(f"Vocab size: {profile.emotion_vocabulary_size}")
        print(f"Self-regulation: {profile.self_regulation_ability}")
        print(f"Strategies: {model.get_regulation_strategy()}")
