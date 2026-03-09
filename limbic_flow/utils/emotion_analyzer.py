"""
情绪分析工具 - 用于分析和可视化情绪状态

[设计原则]
- 更人性化的描述
- 上下文感知
- 渐进式表达
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class EmotionLabel(Enum):
    """情绪标签"""
    JOY = "joy"              # 喜悦
    SADNESS = "sadness"      # 悲伤
    ANGER = "anger"          # 愤怒
    FEAR = "fear"           # 恐惧
    SURPRISE = "surprise"   # 惊讶
    DISGUST = "disgust"     # 厌恶
    NEUTRAL = "neutral"     # 中性
    EXCITEMENT = "excitement"  # 兴奋
    CALM = "calm"           # 平静
    ANXIETY = "anxiety"     # 焦虑
    EMBARRASSMENT = "embarrassment"  # 尴尬
    LONGING = "longing"     # 向往


@dataclass
class EmotionAnalysis:
    """情绪分析结果"""
    primary_emotion: EmotionLabel
    secondary_emotions: List[EmotionLabel] = field(default_factory=list)
    intensity: float  # 0-1
    description: str
    internal_monologue: str  # 内心独白，更人性化
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_emotion": self.primary_emotion.value,
            "secondary_emotions": [e.value for e in self.secondary_emotions],
            "intensity": self.intensity,
            "description": self.description,
            "internal_monologue": self.internal_monologue,
            "suggestions": self.suggestions
        }


class EmotionAnalyzer:
    """
    情绪分析器 - 将 PAD 值转换为可读的情绪描述
    
    [设计]
    - 多维度分析（主要+次要情绪）
    - 内心独白（更自然的表达）
    - 上下文感知
    """
    
    # 情绪映射规则
    EMOTION_MATRIX = {
        # (pleasure_range, arousal_range, dominance_range) -> (emotion, description)
        ((0.5, 1.0), (0.3, 1.0), (-1.0, 1.0)): (EmotionLabel.EXCITEMENT, "你看起来很兴奋！有什么好事发生了吗？"),
        ((0.5, 1.0), (-0.3, 0.3), (-1.0, 1.0)): (EmotionLabel.JOY, "你心情不错，笑容满面的~"),
        ((0.0, 0.5), (0.5, 1.0), (-1.0, 1.0)): (EmotionLabel.EXCITEMENT, "你看起来有点激动，发生了什么？"),
        ((-0.5, 0.0), (0.3, 1.0), (-1.0, -0.3)): (EmotionLabel.ANXIETY, "你看起来有点担心...有什么心事吗？"),
        ((-0.5, 0.0), (0.3, 1.0), (0.3, 1.0)): (EmotionLabel.ANGER, "你看起来有点不爽，谁惹到你了？"),
        ((-1.0, -0.3), (-0.3, 0.3), (-1.0, 1.0)): (EmotionLabel.SADNESS, "你看起来有点低落...想聊聊吗？"),
        ((-1.0, -0.5), (-0.3, 0.3), (-1.0, 1.0)): (EmotionLabel.SADNESS, "你看起来挺伤心的...抱抱你"),
        ((-0.3, 0.3), (0.5, 1.0), (-1.0, 1.0)): (EmotionLabel.SURPRISE, "哇，你看起来很惊讶！"),
        ((-0.3, 0.3), (-0.5, -0.3), (-1.0, 1.0)): (EmotionLabel.CALM, "你看起来很平静，很放松的样子"),
        ((-0.3, 0.3), (-0.3, 0.3), (-0.3, 0.3)): (EmotionLabel.NEUTRAL, "你看起来波澜不惊"),
    }
    
    # 内心独白模板
    MONOLOGUE_TEMPLATES = {
        EmotionLabel.JOY: [
            "哎呀，今天心情真好！",
            "感觉整个人都轻快了~",
            "嘿嘿，有什么好事要发生了吗？",
        ],
        EmotionLabel.SADNESS: [
            "唉...心里有点沉重",
            "不知道为什么，有点难过...",
            "要是能开心一点就好了",
        ],
        EmotionLabel.ANXIETY: [
            "总感觉有什么事情要发生...",
            "心里七上八下的，安静不下来",
            "有点不安，说不清为什么",
        ],
        EmotionLabel.EXCITEMENT: [
            "哇！好激动！",
            "感觉血液都在沸腾！",
            "太兴奋了，根本停不下来！",
        ],
        EmotionLabel.CALM: [
            "就这样静静地...挺好的",
            "岁月静好，现世安稳",
            "平静如水，与世无争",
        ],
        EmotionLabel.ANGER: [
            "哼！生气！",
            "凭什么啊？真的火大",
            "越想越气咽不下这口气",
        ],
        EmotionLabel.SURPRISE: [
            "哎？什么？！",
            "完全没想到会这样！",
            "等等，让我缓缓...",
        ],
        EmotionLabel.NEUTRAL: [
            "嗯...就这样吧",
            "没什么特别的感觉",
            "平平淡淡才是真",
        ],
    }
    
    @classmethod
    def analyze(
        cls,
        pleasure: float,
        arousal: float, 
        dominance: float,
        dopamine: float = 0.5,
        cortisol: float = 0.3,
        context: Dict[str, Any] = None
    ) -> EmotionAnalysis:
        """
        分析情绪状态
        
        Args:
            pleasure: 愉悦度 [-1, 1]
            arousal: 唤醒度 [-1, 1]
            dominance: 控制度 [-1, 1]
            dopamine: 多巴胺 [0, 1]
            cortisol: 皮质醇 [0, 1]
            context: 额外上下文
        
        Returns:
            EmotionAnalysis: 分析结果
        """
        context = context or {}
        
        # 1. 分类主要情绪
        primary_emotion, description = cls._classify_emotion(
            pleasure, arousal, dominance
        )
        
        # 2. 分类次要情绪
        secondary = cls._classify_secondary(
            pleasure, arousal, dominance, dopamine, cortisol
        )
        
        # 3. 计算强度
        intensity = cls._calculate_intensity(
            pleasure, arousal, dominance
        )
        
        # 4. 生成内心独白
        internal_monologue = cls._generate_monologue(
            primary_emotion, secondary, context
        )
        
        # 5. 生成建议
        suggestions = cls._generate_suggestions(
            pleasure, arousal, dominance, dopamine, cortisol, context
        )
        
        return EmotionAnalysis(
            primary_emotion=primary_emotion,
            secondary_emotions=secondary,
            intensity=intensity,
            description=description,
            internal_monologue=internal_monologue,
            suggestions=suggestions
        )
    
    @classmethod
    def _classify_emotion(cls, pleasure: float, arousal: float, dominance: float):
        """分类主要情绪"""
        # 遍历情绪矩阵找匹配
        for (p_range, a_range, d_range), (emotion, desc) in cls.EMOTION_MATRIX.items():
            if p_range[0] <= pleasure <= p_range[1]:
                if a_range[0] <= arousal <= a_range[1]:
                    if d_range[0] <= dominance <= d_range[1]:
                        return emotion, desc
        
        return EmotionLabel.NEUTRAL, "你的情绪有点复杂，说不清楚..."
    
    @classmethod
    def _classify_secondary(cls, pleasure: float, arousal: float, dominance: float, dopamine: float, cortisol: float) -> List[EmotionLabel]:
        """分类次要情绪"""
        secondary = []
        
        # 基于神经递质的次要情绪
        if dopamine > 0.7:
            secondary.append(EmotionLabel.LONGING)
        if dopamine < 0.3:
            secondary.append(EmotionLabel.SADNESS)
        
        if cortisol > 0.7:
            secondary.append(EmotionLabel.ANXIETY)
        
        # 基于PAD组合
        if pleasure > 0.3 and arousal > 0.3:
            if EmotionLabel.EXCITEMENT not in secondary:
                secondary.append(EmotionLabel.JOY)
        
        if dominance < -0.5 and arousal > 0.3:
            secondary.append(EmotionLabel.FEAR)
        
        return secondary[:2]  # 最多2个次要情绪
    
    @classmethod
    def _calculate_intensity(cls, pleasure: float, arousal: float, dominance: float) -> float:
        """计算情绪强度"""
        # 使用向量长度作为强度
        import math
        intensity = math.sqrt(pleasure**2 + arousal**2 + dominance**2) / math.sqrt(3)
        return min(1.0, max(0.0, intensity))
    
    @classmethod
    def _generate_monologue(cls, primary: EmotionLabel, secondary: List[EmotionLabel], context: Dict[str, Any]) -> str:
        """生成内心独白"""
        templates = cls.MONOLOGUE_TEMPLATES.get(primary, cls.MONOLOGUE_TEMPLATES[EmotionLabel.NEUTRAL])
        
        # 加入次要情绪的影响
        if secondary:
            secondary_templates = []
            for s in secondary:
                secondary_templates.extend(cls.MONOLOGUE_TEMPLATES.get(s, []))
            if secondary_templates:
                templates = secondary_templates + templates
        
        return random.choice(templates)
    
    @classmethod
    def _generate_suggestions(cls, pleasure: float, arousal: float, dominance: float, dopamine: float, cortisol: float, context: Dict[str, Any]) -> List[str]:
        """生成建议"""
        suggestions = []
        
        # 基于皮质醇
        if cortisol > 0.7:
            suggestions.append("你看起来压力很大，深呼吸一下？")
        elif cortisol > 0.5:
            suggestions.append("有点紧张，放轻松~")
        
        # 基于愉悦度
        if pleasure < -0.3:
            suggestions.append("有什么心事可以说说看")
        elif pleasure > 0.5:
            suggestions.append("分享你的开心事，让我一起高兴高兴！")
        
        # 基于唤醒度
        if arousal > 0.7:
            suggestions.append("你太激动了，先冷静一下？")
        
        # 基于多巴胺
        if dopamine < 0.3:
            suggestions.append("来点正能量？想想开心的事")
        
        # 基于控制感
        if dominance < -0.5:
            suggestions.append("感觉失控了吗？慢慢来")
        
        return suggestions[:3]  # 最多3条建议


# 便捷函数
def quick_analyze(state: Dict[str, Any], context: Dict[str, Any] = None) -> EmotionAnalysis:
    """快速分析情绪状态"""
    return EmotionAnalyzer.analyze(
        pleasure=state.get("pleasure", 0.0),
        arousal=state.get("arousal", 0.0),
        dominance=state.get("dominance", 0.0),
        dopamine=state.get("dopamine", 0.5),
        cortisol=state.get("cortisol", 0.3),
        context=context
    )
