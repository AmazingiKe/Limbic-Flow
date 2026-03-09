"""
情绪分析工具 - 用于分析和可视化情绪状态
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class EmotionLabel(Enum):
    """情绪标签"""
    HAPPY = "happy"          # 开心
    SAD = "sad"              # 难过
    ANGRY = "angry"          # 生气
    FEARFUL = "fearful"     # 害怕
    SURPRISED = "surprised" # 惊讶
    NEUTRAL = "neutral"     # 中性
    EXCITED = "excited"     # 兴奋
    CALM = "calm"           # 平静
    ANXIOUS = "anxious"     # 焦虑
    RELAXED = "relaxed"     # 放松


@dataclass
class EmotionAnalysis:
    """情绪分析结果"""
    primary_emotion: EmotionLabel
    intensity: float  # 0-1
    description: str
    suggestions: List[str]


class EmotionAnalyzer:
    """
    情绪分析器 - 将 PAD 值转换为可读的情绪描述
    """
    
    @staticmethod
    def analyze(
        pleasure: float,
        arousal: float, 
        dominance: float,
        dopamine: float = 0.5,
        cortisol: float = 0.3
    ) -> EmotionAnalysis:
        """
        分析情绪状态
        
        Args:
            pleasure: 愉悦度 [-1, 1]
            arousal: 唤醒度 [-1, 1]
            dominance: 控制度 [-1, 1]
            dopamine: 多巴胺 [0, 1]
            cortisol: 皮质醇 [0, 1]
        
        Returns:
            EmotionAnalysis: 分析结果
        """
        # 判断主要情绪
        emotion, intensity, description = EmotionAnalyzer._classify_emotion(
            pleasure, arousal, dominance
        )
        
        # 生成建议
        suggestions = EmotionAnalyzer._generate_suggestions(
            pleasure, arousal, dominance, dopamine, cortisol
        )
        
        return EmotionAnalysis(
            primary_emotion=emotion,
            intensity=intensity,
            description=description,
            suggestions=suggestions
        )
    
    @staticmethod
    def _classify_emotion(pleasure: float, arousal: float, dominance: float):
        """分类情绪"""
        
        # 高愉悦 + 高唤醒 = 兴奋
        if pleasure > 0.3 and arousal > 0.3:
            return EmotionLabel.EXCITED, (pleasure + arousal) / 2, "你看起来很兴奋！"
        
        # 高愉悦 + 低唤醒 = 开心
        if pleasure > 0.3 and arousal <= 0.3:
            return EmotionLabel.HAPPY, pleasure, "你心情不错！"
        
        # 低愉悦 + 高唤醒 = 焦虑/害怕
        if pleasure < -0.2 and arousal > 0.3:
            if dominance < 0:
                return EmotionLabel.FEARFUL, (arousal + abs(pleasure)) / 2, "你看起来有点担心"
            return EmotionLabel.ANXIOUS, (arousal + abs(pleasure)) / 2, "你看起来有点焦虑"
        
        # 低愉悦 + 低唤醒 = 悲伤/抑郁
        if pleasure < -0.2 and arousal < 0.2:
            return EmotionLabel.SAD, abs(pleasure), "你看起来有点沮丧"
        
        # 低控制感 = 无助
        if dominance < -0.3:
            return EmotionLabel.ANXIOUS, abs(dominance), "你可能感到一些压力"
        
        # 高唤醒 = 惊讶
        if arousal > 0.5:
            return EmotionLabel.SURPRISED, arousal, "你看起来很惊讶"
        
        # 中性 + 低唤醒 = 平静
        if arousal < 0.2 and abs(pleasure) < 0.3:
            return EmotionLabel.CALM, 1 - arousal, "你看起来很平静"
        
        return EmotionLabel.NEUTRAL, 0.5, "你的情绪比较平稳"
    
    @staticmethod
    def _generate_suggestions(
        pleasure: float,
        arousal: float,
        dominance: float,
        dopamine: float,
        cortisol: float
    ) -> List[str]:
        """生成建议"""
        suggestions = []
        
        # 基于皮质醇
        if cortisol > 0.7:
            suggestions.append("你可能压力比较大，建议深呼吸一下")
        elif cortisol > 0.5:
            suggestions.append("有点压力，可以适当休息一下")
        
        # 基于多巴胺
        if dopamine < 0.3:
            suggestions.append("可能需要一些正向激励")
        
        # 基于愉悦度
        if pleasure < -0.3:
            suggestions.append("有什么我可以帮忙的吗？")
        elif pleasure > 0.5:
            suggestions.append("很高兴你心情这么好！")
        
        # 基于控制感
        if dominance < -0.3:
            suggestions.append("试着掌控一下局面？")
        
        return suggestions
    
    @staticmethod
    def get_mood_color(pleasure: float, arousal: float) -> str:
        """
        获取心情颜色（用于 UI 显示）
        
        Returns:
            hex 颜色代码
        """
        # 简单的颜色映射
        if pleasure > 0.3 and arousal > 0.3:
            return "#FF6B6B"  # 兴奋-红
        if pleasure > 0.3:
            return "#4ECDC4"  # 开心-青
        if pleasure < -0.3 and arousal > 0.3:
            return "#9B59B6"  # 焦虑-紫
        if pleasure < -0.3:
            return "#3498DB"  # 忧郁-蓝
        if arousal > 0.5:
            return "#F39C12"  # 惊讶-橙
        if arousal < -0.3:
            return "#95A5A6"  # 平静-灰
        
        return "#2ECC71"  # 中性-绿


# 便捷函数
def quick_analyze(state: Dict[str, Any]) -> EmotionAnalysis:
    """快速分析情绪状态"""
    return EmotionAnalyzer.analyze(
        pleasure=state.get("pleasure", 0.0),
        arousal=state.get("arousal", 0.0),
        dominance=state.get("dominance", 0.0),
        dopamine=state.get("dopamine", 0.5),
        cortisol=state.get("cortisol", 0.3)
    )
