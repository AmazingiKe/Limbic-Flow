"""
语言与思维系统 - 基于研究文档实现

参考:
- LANGUAGE_THOUGHT.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import re


class MetaphorType(Enum):
    """隐喻类型"""
    ORIENTATION = "orientation"    # 方位
    CONTAINER = "container"       # 容器
    FLUID = "fluid"             # 流体
    FORCE = "force"               # 力量
    BODY = "body"                # 身体


@dataclass
class EmotionalMetaphor:
    """情绪隐喻"""
    metaphor_type: MetaphorType
    source: str                  # 源域
    target: str                  # 目标域
    emotionalvalence: float


class LinguisticRelativity:
    """
    语言相对论
    
    研究: Sapir-Whorf假说
    - 语言影响思维
    - 不同语言使用者有不同的概念
    """
    
    def __init__(self):
        self.language_emotion_mappings = {
            "en": {
                "anger": "hot/fire/burning",
                "sadness": "heavy/dark/cold",
                "joy": "light/bright/warm"
            },
            "zh": {
                "愤怒": "火/燃烧/热气",
                "悲伤": "沉重/阴暗/冰冷",
                "开心": "温暖/明亮/阳光"
            }
        }
    
    def get_language_metaphors(self, emotion: str, language: str) -> List[str]:
        """获取语言特定的情绪隐喻"""
        lang_mappings = self.language_emotion_mappings.get(language, {})
        return lang_mappings.get(emotion, [])


class ConceptualMetaphorTheory:
    """
    概念隐喻理论
    
    研究: Lakoff & Johnson
    - 抽象概念根植于身体经验
    - 情绪隐喻
    """
    
    def __init__(self):
        self.emotion_metaphors = {
            "ANGER": {
                MetaphorType.FLUID: ["boiling", "steaming", "bubbling"],
                MetaphorType.FORCE: ["explosion", "burst", "eruption"],
                MetaphorType.ORIENTATION: ["up", "rising"]
            },
            "SADNESS": {
                MetaphorType.CONTAINER: ["down", "heavy", "dark"],
                MetaphorType.FLUID: ["drain", "empty", "drip"],
                MetaphorType.ORIENTATION: ["down", "low"]
            },
            "JOY": {
                MetaphorType.ORIENTATION: ["up", "light", "floating"],
                MetaphorType.FLUID: ["flowing", "overflowing", "bubbling"]
            },
            "FEAR": {
                MetaphorType.FLUID: ["freezing", "chill"],
                MetaphorType.FORCE: ["crushing", "overwhelming"],
                MetaphorType.CONTAINER: ["enclosed", "trapped"]
            }
        }
    
    def map_emotion_to_metaphors(self, emotion: str) -> Dict[MetaphorType, List[str]]:
        """将情绪映射到隐喻"""
        return self.emotion_metaphors.get(emotion.upper(), {})


class EmotionalLanguageProcessing:
    """
    情绪语言处理
    
    研究: 双向情绪-语言交互
    """
    
    def __init__(self):
        self.positive_lexicon = {}
        self.negative_lexicon = {}
        self.emotion_lexicon = {}
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """分析情感"""
        words = text.lower().split()
        
        pos_count = sum(1 for w in words if w in self.positive_lexicon)
        neg_count = sum(1 for w in words if w in self.negative_lexicon)
        
        total = len(words) or 1
        
        return {
            "positive": pos_count / total,
            "negative": neg_count / total,
            "sentiment": (pos_count - neg_count) / total
        }
    
    def generate_emotional_response(
        self,
        emotion: str,
        intensity: float
    ) -> str:
        """生成情绪化响应"""
        metaphors = ConceptualMetaphorTheory().map_emotion_to_metaphors(emotion)
        
        # 选择隐喻
        if metaphors:
            metaphor_type = list(metaphors.keys())[0]
            metaphor = metaphors[metaphor_type][0]
            
            return f"这让我感到{maybe_metaphor(emotion, intensity)}"
        
        return ""


def maybe_metaphor(emotion: str, intensity: float) -> str:
    """获取情绪隐喻表达"""
    metaphors = {
        "anger": "怒火中烧" if intensity > 0.7 else "有些恼火",
        "sadness": "心情沉重" if intensity > 0.7 else "有些难过",
        "joy": "欣喜若狂" if intensity > 0.7 else "感到开心",
        "fear": "惊恐万分" if intensity > 0.7 else "有些担心"
    }
    return metaphors.get(emotion, "")


class AffectiveDialogueSystem:
    """
    情感对话系统
    """
    
    def __init__(self):
        self.language = LinguisticRelativity()
        self.metaphor = ConceptualMetaphorTheory()
        self.processing = EmotionalLanguageProcessing()
    
    def process_input(self, text: str, language: str = "en") -> Dict:
        """处理输入"""
        sentiment = self.processing.analyze_sentiment(text)
        
        # 提取情绪词
        emotion_words = self._extract_emotion_words(text)
        
        return {
            "sentiment": sentiment,
            "emotions": emotion_words,
            "language": language
        }
    
    def _extract_emotion_words(self, text: str) -> List[str]:
        """提取情绪词"""
        emotion_words = []
        
        emotions = ["happy", "sad", "angry", "fear", "joy", "love", "hate"]
        
        for emotion in emotions:
            if emotion in text.lower():
                emotion_words.append(emotion)
        
        return emotion_words
    
    def generate_response(
        self,
        emotion: str,
        intensity: float
    ) -> str:
        """生成响应"""
        metaphors = self.metaphor.map_emotion_to_metaphors(emotion)
        
        # 使用隐喻生成响应
        return self.processing.generate_emotional_response(emotion, intensity)


if __name__ == "__main__":
    system = AffectiveDialogueSystem()
    result = system.process_input("I am so happy today!")
    print(result)
