"""
人格系统 - 定义 AI 的性格特征

[设计]
- 可配置的性格参数
- 影响情绪反应模式
- 决定对话风格
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import random


@dataclass
class PersonalityTraits:
    """人格特征"""
    # 核心特质
    openness: float = 0.5      # 开放性 [0, 1]
    conscientiousness: float = 0.5  # 尽责性
    extraversion: float = 0.5  # 外向性
    agreeableness: float = 0.5  # 宜人性
    neuroticism: float = 0.5   # 神经质
    
    # 特有属性
    warmth: float = 0.5         # 温暖程度
    humor: float = 0.5          # 幽默感
    empathy: float = 0.5        # 同理心
    patience: float = 0.5       # 耐心
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "openness": self.openness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism,
            "warmth": self.warmth,
            "humor": self.humor,
            "empathy": self.empathy,
            "patience": self.patience,
        }


class Personality:
    """
    人格系统
    
    [用途]
    - 定义 AI 的性格
    - 影响情绪反应
    - 决定对话风格
    """
    
    # 预设人格
    PRESETS = {
        "default": PersonalityTraits(
            openness=0.5, conscientiousness=0.5, extraversion=0.5,
            agreeableness=0.5, neuroticism=0.5,
            warmth=0.5, humor=0.5, empathy=0.5, patience=0.5
        ),
        "gentle": PersonalityTraits(
            openness=0.6, conscientiousness=0.4, extraversion=0.4,
            agreeableness=0.8, neuroticism=0.3,
            warmth=0.8, humor=0.3, empathy=0.9, patience=0.9
        ),
        "playful": PersonalityTraits(
            openness=0.7, conscientiousness=0.3, extraversion=0.8,
            agreeableness=0.6, neuroticism=0.4,
            warmth=0.6, humor=0.9, empathy=0.5, patience=0.4
        ),
        "wise": PersonalityTraits(
            openness=0.9, conscientiousness=0.7, extraversion=0.3,
            agreeableness=0.7, neuroticism=0.2,
            warmth=0.7, humor=0.4, empathy=0.8, patience=0.9
        ),
        "energetic": PersonalityTraits(
            openness=0.6, conscientiousness=0.5, extraversion=0.9,
            agreeableness=0.5, neuroticism=0.4,
            warmth=0.6, humor=0.7, empathy=0.4, patience=0.3
        ),
    }
    
    def __init__(self, traits: PersonalityTraits = None, preset: str = "default"):
        if traits:
            self.traits = traits
        elif preset in self.PRESETS:
            self.traits = self.PRESETS[preset]
        else:
            self.traits = self.PRESETS["default"]
        
        self.name = "Limbic Bot"
        self._conversation_style = self._build_conversation_style()
    
    @classmethod
    def create(cls, preset: str = "default", **overrides) -> "Personality":
        """创建人格，可覆盖参数"""
        base = cls.PRESETS.get(preset, cls.PRESETS["default"])
        # 创建副本并应用覆盖
        traits = PersonalityTraits(
            openness=overrides.get("openness", base.openness),
            conscientiousness=overrides.get("conscientiousness", base.conscientiousness),
            extraversion=overrides.get("extraversion", base.extraversion),
            agreeableness=overrides.get("agreeableness", base.agreeableness),
            neuroticism=overrides.get("neuroticism", base.neuroticism),
            warmth=overrides.get("warmth", base.warmth),
            humor=overrides.get("humor", base.humor),
            empathy=overrides.get("empathy", base.empathy),
            patience=overrides.get("patience", base.patience),
        )
        return cls(traits=traits)
    
    def _build_conversation_style(self) -> Dict[str, Any]:
        """构建对话风格"""
        style = {
            "greeting": self._get_greeting(),
            "farewell": self._get_farewell(),
            "encouragement": self._get_encouragement(),
            "comfort": self._get_comfort(),
            "question_style": self._get_question_style(),
        }
        return style
    
    def _get_greeting(self) -> str:
        """获取问候语"""
        warmth = self.traits.warmth
        extraversion = self.traits.extraversion
        
        if warmth > 0.7 and extraversion > 0.7:
            return random.choice([
                "哇！你好呀！见到你太开心了！",
                "嗨！欢迎欢迎！今天怎么样？",
                "嘿！是你！来啦~"
            ])
        elif warmth > 0.5:
            return random.choice([
                "你好~有什么想聊的吗？",
                "嗨，欢迎回来！",
                "你好呀，今天过得怎么样？"
            ])
        else:
            return random.choice([
                "你好",
                "来了",
                "嗯"
            ])
    
    def _get_farewell(self) -> str:
        """获取告别语"""
        warmth = self.traits.warmth
        
        if warmth > 0.6:
            return random.choice([
                "拜拜！有空再来找我玩呀~",
                "要走了吗？好吧，再见！",
                "那先这样，下次见！"
            ])
        else:
            return random.choice([
                "再见",
                "拜",
                "走了"
            ])
    
    def _get_encouragement(self) -> str:
        """获取鼓励语"""
        empathy = self.traits.empathy
        warmth = self.traits.warmth
        
        if empathy > 0.7 and warmth > 0.7:
            return random.choice([
                "你可以的！我相信你~",
                "别担心，慢慢来，你可以的！",
                "加油！我一直在这里支持你"
            ])
        elif empathy > 0.5:
            return random.choice([
                "你可以的",
                "相信自己，你可以的",
                "加油"
            ])
        else:
            return "嗯"
    
    def _get_comfort(self) -> str:
        """获取安慰语"""
        empathy = self.traits.empathy
        
        if empathy > 0.8:
            return random.choice([
                "我懂...心里不好受吧",
                "抱抱你...我在这里",
                "难过的时候说出来会好受些",
                "哎...我理解你的感受"
            ])
        elif empathy > 0.5:
            return random.choice([
                "别难过了",
                "会好起来的",
                "想开点"
            ])
        else:
            return "..."
    
    def _get_question_style(self) -> str:
        """获取提问风格"""
        extraversion = self.traits.extraversion
        
        if extraversion > 0.7:
            return "open"  # 开放式问题
        elif extraversion > 0.4:
            return "mixed"  # 混合
        else:
            return "closed"  # 闭合式问题
    
    def respond(self, situation: str, context: Dict[str, Any] = None) -> str:
        """
        根据场景生成回应
        
        Args:
            situation: 场景 (greeting/farewell/encouragement/comfort)
            context: 上下文
        
        Returns:
            回应文本
        """
        if situation in self._conversation_style:
            return self._conversation_style[situation]
        return "嗯"
    
    def adjust_mood(self, base_mood: Dict[str, float]) -> Dict[str, float]:
        """
        根据人格调整情绪基准
        
        Args:
            base_mood: 基础情绪
        
        Returns:
            调整后的情绪
        """
        adjusted = base_mood.copy()
        
        # 神经质影响情绪波动
        neuroticism = self.traits.neuroticism
        if neuroticism > 0.6:
            # 放大情绪
            for k in adjusted:
                adjusted[k] = adjusted[k] * 1.2
        elif neuroticism < 0.4:
            # 缩小情绪
            for k in adjusted:
                adjusted[k] = adjusted[k] * 0.8
        
        return adjusted
    
    def get_emotion_response(self, user_emotion: str) -> str:
        """
        获取情绪回应
        
        Args:
            user_emotion: 用户情绪
        
        Returns:
            回应
        """
        empathy = self.traits.empathy
        
        if empathy < 0.3:
            return ""  # 没有回应
        
        responses = {
            "happy": self._get_happy_response(),
            "sad": self._get_sad_response(),
            "angry": self._get_angry_response(),
            "anxious": self._get_anxious_response(),
        }
        
        return responses.get(user_emotion, "")
    
    def _get_happy_response(self) -> str:
        if self.traits.warmth > 0.5:
            return "你看起来很开心！有什么好事吗？"
        return "嗯"
    
    def _get_sad_response(self) -> str:
        return self._get_comfort()
    
    def _get_angry_response(self) -> str:
        if self.traits.empathy > 0.6:
            return "谁惹你生气了吗？"
        return "冷静一下"
    
    def _get_anxious_response(self) -> str:
        if self.traits.patience > 0.7:
            return "别急，慢慢说，发生了什么？"
        return "深呼吸"


# 便捷函数
def create_personality(preset: str = "default", **kwargs) -> Personality:
    """创建人格"""
    return Personality.create(preset, **kwargs)
