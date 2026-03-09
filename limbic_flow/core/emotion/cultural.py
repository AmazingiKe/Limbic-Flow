"""
跨文化情绪建模 - 基于研究文档实现

参考:
- CULTURAL_EMOTION_MODELING.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random


class CultureType(Enum):
    """文化类型"""
    WESTERN = "western"         # 西方 (个人主义)
    EAST_ASIAN = "east_asian"   # 东亚 (集体主义)
    LATIN = "latin"           # 拉丁美洲
    MIDDLE_EASTERN = "middle_eastern"  # 中东
    AFRICAN = "african"       # 非洲


class EmotionExpression(Enum):
    """情绪表达风格"""
    DIRECT = "direct"         # 直接表达
    RESTRAINED = "restrained"  # 克制表达
    EXPRESSIVE = "expressive"  # 表达丰富
    MASKED = "masked"        # 掩饰表达


@dataclass
class CulturalProfile:
    """文化配置文件"""
    culture_type: CultureType
    
    # Hofstede 维度
    power_distance: float = 0.5      # 权力距离
    individualism: float = 0.5       # 个人主义
    masculinity: float = 0.5         # 男性气质
    uncertainty_avoidance: float = 0.5  # 不确定性规避
    
    # 情绪表达规则
    expression_style: EmotionExpression = EmotionExpression.DIRECT
    
    # 情绪词汇粒度
    emotion_granularity: float = 0.5  # 0=粗略, 1=细致
    
    # 特定情绪词
    specific_emotions: List[str] = field(default_factory=list)


@dataclass
class EmotionExpressionResult:
    """情绪表达结果"""
    modified_intensity: float
    display_rule: str
    recommended_expression: str


class CulturalEmotionSystem:
    """
    跨文化情绪系统
    
    研究:
    - 文化情绪规范
    - 情绪表达差异
    - 普遍 vs 文化情绪
    """
    
    def __init__(self):
        self.current_culture = CultureType.WESTERN
        self.culture_profiles = self._init_cultures()
        
        # 文化特定词汇
        self.emotion_lexicons = self._init_lexicons()
    
    def _init_cultures(self) -> Dict[CultureType, CulturalProfile]:
        """初始化文化配置"""
        return {
            CultureType.WESTERN: CulturalProfile(
                culture_type=CultureType.WESTERN,
                power_distance=0.4,
                individualism=0.8,
                masculinity=0.6,
                uncertainty_avoidance=0.5,
                expression_style=EmotionExpression.DIRECT,
                emotion_granularity=0.8
            ),
            CultureType.EAST_ASIAN: CulturalProfile(
                culture_type=CultureType.EAST_ASIAN,
                power_distance=0.7,
                individualism=0.3,
                masculinity=0.4,
                uncertainty_avoidance=0.7,
                expression_style=EmotionExpression.RESTRAINED,
                emotion_granularity=0.6,
                specific_emotions=[" vergüenza", "pena"]
            ),
            CultureType.LATIN: CulturalProfile(
                culture_type=CultureType.LATIN,
                power_distance=0.5,
                individualism=0.5,
                masculinity=0.5,
                uncertainty_avoidance=0.5,
                expression_style=EmotionExpression.EXPRESSIVE,
                emotion_granularity=0.7
            ),
            CultureType.MIDDLE_EASTERN: CulturalProfile(
                culture_type=CultureType.MIDDLE_EASTERN,
                power_distance=0.7,
                individualism=0.3,
                masculinity=0.6,
                uncertainty_avoidance=0.6,
                expression_style=EmotionExpression.RESTRAINED,
                emotion_granularity=0.5
            ),
            CultureType.AFRICAN: CulturalProfile(
                culture_type=CultureType.AFRICAN,
                power_distance=0.6,
                individualism=0.4,
                masculinity=0.4,
                uncertainty_avoidance=0.5,
                expression_style=EmotionExpression.EXPRESSIVE,
                emotion_granularity=0.5
            ),
        }
    
    def _init_lexicons(self) -> Dict[CultureType, Dict[str, List[str]]]:
        """初始化情绪词汇"""
        return {
            CultureType.WESTERN: {
                "anger": ["angry", "furious", "irritated"],
                "sadness": ["sad", "depressed", "upset"],
                "joy": ["happy", "excited", "delighted"]
            },
            CultureType.EAST_ASIAN: {
                "anger": ["生气", "愤怒", "恼火"],
                "sadness": ["悲伤", "忧郁", "难过"],
                "joy": ["开心", "高兴", "愉快"]
            },
            CultureType.LATIN: {
                "anger": ["enojado", "furioso", "molesto"],
                "sadness": ["triste", "apenado", "melancólico"],
                "joy": ["feliz", "contento", "alegre"]
            }
        }
    
    def set_culture(self, culture: CultureType):
        """设置当前文化"""
        self.current_culture = culture
    
    def adjust_expression(
        self,
        emotion: str,
        base_intensity: float,
        context: Dict
    ) -> EmotionExpressionResult:
        """
        调整情绪表达
        
        研究: 不同文化有不同的显示规则
        """
        profile = self.culture_profiles[self.current_culture]
        
        # 根据表达风格调整强度
        modified = base_intensity
        
        if profile.expression_style == EmotExpression.RESTRAINED:
            # 克制表达: 降低强度
            modified = base_intensity * 0.6
            
        elif profile.expression_style == EmotionExpression.EXPRESSIVE:
            # 表达丰富: 增强强度
            modified = base_intensity * 1.3
        
        elif profile.expression_style == EmotionExpression.MASKED:
            # 掩饰表达: 微笑掩盖负面情绪
            if base_intensity < 0:
                modified = -base_intensity * 0.3  # 转为轻微正面
            else:
                modified = base_intensity * 0.8
        
        # 根据权力距离调整对权威的情绪
        if context.get("target_authority", False):
            if profile.power_distance > 0.6:
                # 高权力距离: 减弱负面表达
                modified *= 0.5
        
        # 获取显示规则
        display_rule = self._get_display_rule(emotion, profile)
        
        # 推荐表达方式
        recommended = self._get_recommended_expression(emotion, profile)
        
        return EmotionExpressionResult(
            modified_intensity=max(0, min(1, modified)),
            display_rule=display_rule,
            recommended_expression=recommended
        )
    
    def _get_display_rule(self, emotion: str, profile: CulturalProfile) -> str:
        """获取显示规则"""
        if profile.expression_style == EmotionExpression.RESTRAINED:
            return "suppress_negative_express_positive"
        elif profile.expression_style == EmotionExpression.MASKED:
            return "mask_with_neutral"
        else:
            return "express_authentically"
    
    def _get_recommended_expression(
        self, 
        emotion: str, 
        profile: CulturalProfile
    ) -> str:
        """获取推荐表达"""
        lexicon = self.emotion_lexicons.get(
            self.current_culture, 
            self.emotion_lexicons[CultureType.WESTERN]
        )
        
        words = lexicon.get(emotion, ["emotion"])
        
        # 根据粒度选择词汇
        if profile.emotion_granularity > 0.7:
            return words[0]  # 最细致的词
        else:
            return words[-1]  # 更通用的词
    
    def get_cultural_emotion_words(
        self,
        emotion_category: str
    ) -> List[str]:
        """获取文化特定情绪词"""
        lexicon = self.emotion_lexicons.get(
            self.current_culture,
            self.emotion_lexicons[CultureType.WESTERN]
        )
        
        return lexicon.get(emotion_category, [])


class UniversalEmotionDetector:
    """
    普遍情绪检测器
    
    研究: Ekman的6种普遍情绪
    - Happiness, Sadness, Anger, Fear, Surprise, Disgust
    """
    
    # 普遍情绪
    UNIVERSAL_EMOTIONS = [
        "happiness", "sadness", "anger", 
        "fear", "surprise", "disgust"
    ]
    
    # 文化特定情绪
    CULTURAL_SPECIFIC = {
        CultureType.EAST_ASIAN: [" vergüenza", "k reserves"],
        CultureType.LATIN: ["simpatía", "morriña"],
    }
    
    def detect(
        self,
        expression: Dict
    ) -> Dict[str, float]:
        """
        检测情绪
        
        Returns:
            Dict: 情绪及其强度
        """
        # 简化的面部表情检测
        results = {}
        
        # 普遍情绪
        for emotion in self.UNIVERSAL_EMOTIONS:
            results[emotion] = expression.get(emotion, 0.0)
        
        return results
    
    def is_cultural_emotion(self, emotion: str) -> bool:
        """判断是否为文化特定情绪"""
        for specific_list in self.CULTURAL_SPECIFIC.values():
            if emotion in specific_list:
                return True
        return False


class EmotionMetaphorMapper:
    """
    情绪隐喻映射器
    
    研究: 不同文化使用不同隐喻描述情绪
    - 愤怒 = 热 (很多文化)
    - 悲伤 = 沉重 (西方)
    """
    
    # 文化隐喻映射
    ANGER_METAPHORS = {
        CultureType.WESTERN: ["hot", "burning", "fire"],
        CultureType.EAST_ASIAN: ["火", "燃烧", "热气"],
        CultureType.LATIN: ["fuego", "caliente"],
    }
    
    SADNESS_METAPHORS = {
        CultureType.WESTERN: ["heavy", "dark", "cold"],
        CultureType.EAST_ASIAN: ["沉重", "阴暗", "冰冷"],
    }
    
    def get_metaphor(self, emotion: str) -> List[str]:
        """获取情绪隐喻"""
        if emotion in ["anger", "愤怒"]:
            return self.ANGER_METAPHORS.get(
                self.current_culture,
                self.ANGER_METAPHORS[CultureType.WESTERN]
            )
        elif emotion in ["sadness", "悲伤"]:
            return self.SADNESS_METAPHORS.get(
                self.current_culture,
                self.SADNESS_METAPHORS[CultureType.WESTERN]
            )
        
        return []


# 示例
if __name__ == "__main__":
    # 创建跨文化系统
    system = CulturalEmotionSystem()
    
    # 设置东亚文化
    system.set_culture(CultureType.EAST_ASIAN)
    
    # 调整表达
    result = system.adjust_expression(
        "anger",
        0.8,
        {"target_authority": True}
    )
    
    print(f"Original intensity: 0.8")
    print(f"Modified intensity: {result.modified_intensity}")
    print(f"Display rule: {result.display_rule}")
    print(f"Recommended: {result.recommended_expression}")
