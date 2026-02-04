from typing import Dict, Optional, Any
import os
import torch
import soundfile as sf
import asyncio
from limbic_flow.core.articulation.tts.base import TTSBackend

# 尝试导入，如果环境没准备好则报错
try:
    from qwen_tts import Qwen3TTSModel
    HAS_QWEN = True
except ImportError:
    HAS_QWEN = False

class QwenLocalTTS(TTSBackend):
    """
    Qwen3-TTS 本地模型后端
    使用 Qwen3-TTS-12Hz-1.7B-VoiceDesign 进行基于指令的语音生成
    """

    def __init__(self, model_path: str = "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device: str = "cuda:0"):
        if not HAS_QWEN:
            raise ImportError("请先安装 qwen-tts: `pip install -U qwen-tts`")

        print(f"🔄 [QwenTTS] Loading model from {model_path} on {device}...")
        self.model = Qwen3TTSModel.from_pretrained(
            model_path,
            device_map=device,
            dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
        )
        print("✅ [QwenTTS] Model loaded successfully.")

    @property
    def provider_name(self) -> str:
        return "qwen_local"

    async def generate(self, text: str, output_path: str, emotion_state: Optional[Dict[str, float]] = None) -> str:
        """
        生成语音文件
        """
        # 1. 构建指令 (Instruction)
        instruct = self._build_instruct_from_emotion(emotion_state or {})
        print(f"🎙️ [QwenTTS] Generating with instruct: '{instruct}'")

        # 2. 运行推理 (在线程池中运行以防阻塞事件循环)
        # 注意：这里简化处理，直接调用同步方法，生产环境建议用 run_in_executor
        try:
            wavs, sr = self.model.generate_voice_design(
                text=text,
                language="Chinese", # 默认中文，未来可配置
                instruct=instruct
            )

            # 3. 保存文件
            sf.write(output_path, wavs[0], sr)
            return output_path

        except Exception as e:
            print(f"❌ [QwenTTS] Generation failed: {e}")
            raise

    async def speak(self, text: str, emotion_state: Optional[Dict[str, float]] = None):
        """
        生成并播放
        """
        # 生成临时文件
        temp_path = "temp_speech.wav"
        await self.generate(text, temp_path, emotion_state)

        # 播放 (使用简单的系统命令，跨平台可能需要调整)
        print(f"🔊 [QwenTTS] Playing audio...")
        if os.name == 'posix': # Mac/Linux
            os.system(f"afplay {temp_path}" if os.uname().sysname == 'Darwin' else f"aplay {temp_path}")
        else: # Windows
            # Windows 播放 wav 有点麻烦，可以用 powershell
            os.system(f'powershell -c (New-Object Media.SoundPlayer "{temp_path}").PlaySync();')

    def _build_instruct_from_emotion(self, emotion: Dict[str, float]) -> str:
        """
        将 PAD 情绪值转换为自然语言指令 (Prompt Engineering for Audio)
        """
        pleasure = emotion.get('pleasure', 0.0)
        arousal = emotion.get('arousal', 0.0)
        dominance = emotion.get('dominance', 0.0)

        # 基础音色设定 (可以做成可配置的)
        base_voice = "年轻女性声音，音色清澈自然"

        descriptors = []

        # Pleasure (愉悦度)
        if pleasure > 0.6:
            descriptors.append("充满喜悦和热情")
        elif pleasure > 0.2:
            descriptors.append("语气轻松愉快")
        elif pleasure < -0.6:
            descriptors.append("极度悲伤，带有哭腔")
        elif pleasure < -0.2:
            descriptors.append("语气低落忧郁")

        # Arousal (唤醒度) - 影响语速和能量
        if arousal > 0.6:
            descriptors.append("语速较快，能量充沛，情绪激动")
        elif arousal > 0.2:
            descriptors.append("语速轻快")
        elif arousal < -0.6:
            descriptors.append("语速缓慢，有气无力，甚至有停顿")
        elif arousal < -0.2:
            descriptors.append("语速舒缓平静")

        # Dominance (控制度) - 影响自信和语气强弱
        if dominance > 0.5:
            descriptors.append("语气坚定自信，不容置疑")
        elif dominance < -0.5:
            descriptors.append("语气怯懦，小心翼翼，缺乏自信")

        # 组合指令
        instruct_suffix = "，".join(descriptors)
        if not instruct_suffix:
            instruct_suffix = "语气平和自然"

        return f"{base_voice}，{instruct_suffix}。"
