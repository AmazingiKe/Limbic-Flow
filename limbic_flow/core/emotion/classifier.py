"""
情绪识别系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict, List
import random


@dataclass
class EmotionCluster:
    """情绪簇"""
    name: str
    base_emotions: List[str]
    description: str


class EmotionClassifier:
    """情绪分类器"""
    
    # Ekman 基础情绪
    BASIC_EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
    
    # Plutchik 情绪轮
    EMOTION_WHEEL = {
        "joy": ["serenity", "ecstasy"],
        "sadness": ["pensiveness", "grief"],
        "anger": ["annoyance", "rage"],
        "fear": ["apprehension", "terror"],
        "surprise": ["distraction", "amazement"],
        "disgust": ["boredom", "loathing"],
    }
    
    def __init__(self):
        self.emotion_clusters = self._init_clusters()
    
    def _init_clusters(self) -> Dict[str, EmotionCluster]:
        return {
            "positive_high": EmotionCluster("positive_high", ["joy", "ecstasy"], "高唤醒积极"),
            "positive_low": EmotionCluster("positive_low", ["serenity", "contentment"], "低唤醒积极"),
            "negative_high": EmotionCluster("negative_high", ["anger", "rage", "fear", "terror"], "高唤醒消极"),
            "negative_low": EmotionCluster("negative_low", ["sadness", "grief", "boredom"], "低唤醒消极"),
        }
    
    def classify(self, emotion_vector: Dict[str, float]) -> str:
        """分类情绪"""
        valence = emotion_vector.get("valence", 0)
        arousal = emotion_vector.get("arousal", 0.5)
        
        if valence > 0.3:
            return "positive" if arousal < 0.5 else "excited"
        elif valence < -0.3:
            return "negative" if arousal < 0.5 else "anxious"
        
        return "neutral"
    
    def get_intensity_level(self, intensity: float) -> str:
        """获取强度等级"""
        if intensity > 0.8:
            return "intense"
        elif intensity > 0.5:
            return "moderate"
        else:
            return "mild"


class EmotionRecognizer:
    """情绪识别器"""
    
    def __init__(self):
        self.classifier = EmotionClassifier()
    
    def recognize_from_text(self, text: str) -> Dict[str, float]:
        """从文本识别"""
        text_lower = text.lower()
        
        emotions = {}
        
        emotion_keywords = {
            "joy": ["开心", "高兴", "快乐", "happy", "joy"],
            "sadness": ["难过", "伤心", "sad", "sadness"],
            "anger": ["生气", "愤怒", "angry", "anger"],
            "fear": ["害怕", "担心", "fear", "afraid"],
        }
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            if count > 0:
                emotions[emotion] = min(1.0, count * 0.5)
        
        return emotions
    
    def recognize_from_physiology(self, signals: Dict) -> Dict[str, float]:
        """从生理信号识别"""
        emotions = {}
        
        heart_rate = signals.get("heart_rate", 70)
        gsr = signals.get("gsr", 0)
        
        if heart_rate > 90:
            emotions["arousal"] = 0.8
        if gsr > 0.5:
            emotions["stress"] = 0.7
        
        return emotions


if __name__ == "__main__":
    recognizer = EmotionRecognizer()
    result = recognizer.recognize_from_text("我很开心!")
    print(result)
