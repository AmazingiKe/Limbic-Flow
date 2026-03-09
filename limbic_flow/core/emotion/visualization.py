"""
情绪可视化系统
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class EmotionVisualization:
    """情绪可视化数据"""
    type: str
    data: Dict
    color: str


class EmotionVisualizer:
    """情绪可视化器"""
    
    EMOTION_COLORS = {
        "joy": "#FFD700",
        "sadness": "#4169E1",
        "anger": "#FF4500",
        "fear": "#9370DB",
        "surprise": "#00CED1",
        "disgust": "#32CD32",
    }
    
    def visualize_as_meter(self, emotion: str, intensity: float) -> EmotionVisualization:
        """仪表盘可视化"""
        return EmotionVisualization(
            type="meter",
            data={"emotion": emotion, "intensity": intensity},
            color=self.EMOTION_COLORS.get(emotion, "#808080")
        )
    
    def visualize_as_dial(self, pad: Dict) -> EmotionVisualization:
        """刻度盘可视化"""
        return EmotionVisualization(
            type="dial",
            data={"pleasure": pad.get("pleasure", 0), "arousal": pad.get("arousal", 0)},
            color="#FF6347"
        )
    
    def visualize_as_timeline(self, history: List[Dict]) -> EmotionVisualization:
        """时间线可视化"""
        return EmotionVisualization(
            type="timeline",
            data={"points": history},
            color="#4682B4"
        )


class EmotionRenderer:
    """情绪渲染器"""
    
    def __init__(self):
        self.visualizer = EmotionVisualizer()
    
    def render_emoji(self, emotion: str) -> str:
        """渲染表情"""
        emoji_map = {
            "joy": "😊",
            "sadness": "😢",
            "anger": "😠",
            "fear": "😨",
            "surprise": "😲",
            "disgust": "🤢",
        }
        return emoji_map.get(emotion, "😐")
    
    def render_color(self, emotion: str) -> str:
        """渲染颜色"""
        return self.visualizer.EMOTION_COLORS.get(emotion, "#808080")


if __name__ == "__main__":
    renderer = EmotionRenderer()
    print(renderer.render_emoji("joy"))
