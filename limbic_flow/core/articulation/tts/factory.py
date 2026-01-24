import os
from typing import Optional
from limbic_flow.core.articulation.tts.base import TTSBackend
from limbic_flow.core.articulation.tts.backends.mock import MockTTS

# 未来在这里导入其他后端
# from limbic_flow.core.articulation.tts.backends.openai import OpenAITTS
# from limbic_flow.core.articulation.tts.backends.qwen import QwenTTS

class TTSFactory:
    """
    TTS 工厂类 - 负责实例化具体的 TTS 后端
    """

    @staticmethod
    def create(provider: Optional[str] = None) -> TTSBackend:
        """
        创建 TTS 实例

        Args:
            provider: 指定的提供商名称 (mock, openai, qwen, edge)
                      如果为 None，则读取环境变量 LIMBIC_TTS_PROVIDER，默认为 mock
        """
        if not provider:
            provider = os.getenv("LIMBIC_TTS_PROVIDER", "mock").lower()

        if provider == "mock":
            return MockTTS()

        # 预留分支
        # elif provider == "openai":
        #     return OpenAITTS()
        # elif provider == "qwen":
        #     return QwenTTS()

        else:
            print(f"⚠️ 未知的 TTS 提供商 '{provider}'，回退到 Mock 模式")
            return MockTTS()
