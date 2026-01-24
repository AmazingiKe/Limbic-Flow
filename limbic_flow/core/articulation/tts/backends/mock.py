from typing import Dict, Optional
import os
import asyncio
from limbic_flow.core.articulation.tts.base import TTSBackend

class MockTTS(TTSBackend):
    """
    Mock TTS 后端 - 仅用于开发和测试
    不生成实际音频，仅打印日志
    """

    @property
    def provider_name(self) -> str:
        return "mock"

    async def generate(self, text: str, output_path: str, emotion_state: Optional[Dict[str, float]] = None) -> str:
        params = self._map_emotion_to_params(emotion_state or {})
        print(f"🔊 [MockTTS] Generating audio to {output_path}")
        print(f"   Text: {text}")
        print(f"   Emotion Params: {params}")

        # 模拟生成延迟
        await asyncio.sleep(0.5)

        # 创建一个空文件以模拟成功
        with open(output_path, 'w') as f:
            f.write("mock audio content")

        return output_path

    async def speak(self, text: str, emotion_state: Optional[Dict[str, float]] = None):
        params = self._map_emotion_to_params(emotion_state or {})
        print(f"🔊 [MockTTS] Speaking: '{text}'")
        print(f"   > Emotion Context: {emotion_state}")
        print(f"   > Mapped Params: {params}")
        await asyncio.sleep(1.0)
