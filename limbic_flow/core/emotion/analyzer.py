"""
情绪分析系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import statistics


@dataclass
class EmotionAnalysis:
    """情绪分析结果"""
    dominant_emotion: str
    intensity: float
    valence: float
    arousal: float
    stability: float


class EmotionAnalyzer:
    """情绪分析器"""
    
    def __init__(self):
        self.history: List[Dict] = []
    
    def analyze(
        self,
        emotion_state: Dict
    ) -> EmotionAnalysis:
        """分析情绪状态"""
        valence = emotion_state.get("pleasure", 0)
        arousal = emotion_state.get("arousal", 0.5)
        
        # 主导情绪
        dominant = self._get_dominant_emotion(emotion_state)
        
        # 强度
        intensity = abs(valence) + arousal
        intensity = min(1.0, intensity / 2)
        
        # 稳定性
        stability = self._calculate_stability()
        
        return EmotionAnalysis(
            dominant_emotion=dominant,
            intensity=intensity,
            valence=valence,
            arousal=arousal,
            stability=stability
        )
    
    def _get_dominant_emotion(self, state: Dict) -> str:
        """获取主导情绪"""
        emotions = {
            "joy": state.get("joy", 0),
            "sadness": state.get("sadness", 0),
            "anger": state.get("anger", 0),
            "fear": state.get("fear", 0),
            "surprise": state.get("surprise", 0),
            "disgust": state.get("disgust", 0),
        }
        
        return max(emotions, key=emotions.get)
    
    def _calculate_stability(self) -> float:
        """计算稳定性"""
        if len(self.history) < 5:
            return 1.0
        
        recent = self.history[-10:]
        values = [h.get("valence", 0) for h in recent]
        
        if not values:
            return 1.0
        
        std = statistics.stdev(values) if len(values) > 1 else 0
        return max(0, 1 - std * 2)
    
    def add_to_history(self, state: Dict):
        """添加到历史"""
        self.history.append(state)
        if len(self.history) > 100:
            self.history.pop(0)


class TrendAnalyzer:
    """趋势分析器"""
    
    def __init__(self):
        self.window_size = 10
    
    def detect_trend(self, emotions: List[Dict]) -> str:
        """检测趋势"""
        if len(emotions) < 3:
            return "stable"
        
        recent = emotions[-self.window_size:]
        
        valence_trend = self._calculate_trend([e.get("pleasure", 0) for e in recent])
        
        if valence_trend > 0.3:
            return "improving"
        elif valence_trend < -0.3:
            return "declining"
        
        return "stable"
    
    def _calculate_trend(self, values: List[float]) -> float:
        """计算趋势"""
        if len(values) < 2:
            return 0
        
        # 简单线性趋势
        n = len(values)
        x = list(range(n))
        y = values
        
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator


if __name__ == "__main__":
    analyzer = EmotionAnalyzer()
    result = analyzer.analyze({"pleasure": 0.5, "arousal": 0.6})
    print(f"Dominant: {result.dominant_emotion}")
