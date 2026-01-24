from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import os

class TTSBackend(ABC):
    """
    TTS (Text-to-Speech) 后端抽象基类
    所有的 TTS 实现（OpenAI, Qwen-Local, Edge-TTS）都必须继承此类
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供商名称"""
        pass

    @abstractmethod
    async def generate(self, text: str, output_path: str, emotion_state: Optional[Dict[str, float]] = None) -> str:
        """
        生成语音文件

        Args:
            text: 要转换的文本
            output_path: 音频保存路径
            emotion_state: 情绪状态字典 (e.g., {'pleasure': 0.5, 'arousal': 0.8})，用于调整语调/语速

        Returns:
            str: 生成的音频文件绝对路径
        """
        pass

    @abstractmethod
    async def speak(self, text: str, emotion_state: Optional[Dict[str, float]] = None):
        """
        直接播放语音 (即时模式)

        Args:
            text: 要朗读的文本
            emotion_state: 情绪状态
        """
        pass

    def _map_emotion_to_params(self, emotion_state: Dict[str, float]) -> Dict[str, Any]:
        """
        辅助方法：将 PAD 情绪值映射为具体的 TTS 参数 (如 speed, pitch)
        子类可以覆盖此方法以适配特定的模型参数
        """
        if not emotion_state:
            return {}

        params = {}
        # 简单的通用映射示例
        arousal = emotion_state.get('arousal', 0.0)
        pleasure = emotion_state.get('pleasure', 0.0)

        # Arousal (唤醒度) -> 语速
        # High arousal = faster speed
        # Low arousal = slower speed
        if arousal > 0.5:
            params['speed'] = 1.2
        elif arousal < -0.5:
            params['speed'] = 0.8
        else:
            params['speed'] = 1.0

        # Pleasure (愉悦度) -> 语调 (Pitch)
        # (注：这取决于具体引擎是否支持)
        if pleasure > 0.5:
            params['pitch'] = "+10Hz"
        elif pleasure < -0.5:
            params['pitch'] = "-5Hz"

        return params
