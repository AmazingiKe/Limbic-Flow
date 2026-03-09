"""
情绪生成系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict, List
import random


class EmotionGenerator:
    """情绪生成器"""
    
    def __init__(self):
        self.generation_templates = {
            "joy": ["太好了!", "真开心!", "太棒了!"],
            "sadness": ["有点难过...", "心情不好", "沮丧"],
            "anger": ["太气人了!", "真让人生气", "愤怒"],
            "fear": ["好害怕...", "担心", "惊恐"],
        }
    
    def generate_emotional_expression(
        self,
        emotion: str,
        intensity: float,
        style: str = "neutral"
    ) -> str:
        """生成情绪表达"""
        templates = self.generation_templates.get(emotion, ["..."])
        
        if intensity > 0.7:
            prefix = "非常"
        elif intensity < 0.3:
            prefix = "有点"
        else:
            prefix = ""
        
        template = random.choice(templates)
        return prefix + template
    
    def generate_body_language(
        self,
        emotion: str,
        intensity: float
    ) -> Dict[str, str]:
        """生成身体语言"""
        expressions = {
            "joy": {"posture": "upright", "gesture": "open_arms"},
            "sadness": {"posture": "slumped", "gesture": "downcast"},
            "anger": {"posture": "tense", "gesture": "pointing"},
            "fear": {"posture": "tense", "gesture": "protecting"},
        }
        
        return expressions.get(emotion, {"posture": "neutral", "gesture": "none"})


class AffectiveResponseGenerator:
    """情绪响应生成器"""
    
    def __init__(self):
        self.strategies = {
            "validation": "我理解你的感受",
            "support": "我在这里支持你",
            "reflection": "听起来你感到...",
            "exploration": "想多说说吗?",
        }
    
    def generate_response(
        self,
        user_emotion: str,
        strategy: str = "validation"
    ) -> str:
        """生成响应"""
        return self.strategies.get(strategy, "我听到了")
    
    def select_strategy(
        self,
        user_emotion: str,
        conversation_context: Dict
    ) -> str:
        """选择策略"""
        if user_emotion in ["sadness", "fear"]:
            return "validation"
        elif user_emotion == "anger":
            return "reflection"
        
        return "exploration"


class NarrativeEmotionGenerator:
    """叙事情绪生成器"""
    
    def __init__(self):
        self.story_arcs = {
            "hero": {"emotions": ["hope", "fear", "joy", "triumph"]},
            "tragedy": {"emotions": ["hope", "fear", "sadness", "despair"]},
            "romance": {"emotions": ["attraction", "joy", "anxiety", "love"]},
        }
    
    def generate_story_emotions(
        self,
        arc: str,
        progress: float
    ) -> List[str]:
        """生成故事情绪"""
        emotions = self.story_arcs.get(arc, {}).get("emotions", [])
        
        idx = int(progress * len(emotions))
        return emotions[:idx + 1]


if __name__ == "__main__":
    gen = EmotionGenerator()
    print(gen.generate_emotional_expression("joy", 0.8))
