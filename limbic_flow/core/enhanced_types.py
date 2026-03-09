"""
数据类型定义 - 增强版

包含:
- 增强的 CognitiveState
- 消息类型
- 响应类型
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class Message:
    """消息"""
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationContext:
    """对话上下文"""
    messages: List[Message] = field(default_factory=list)
    user_id: str = "default"
    session_id: str = ""
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """添加消息"""
        self.messages.append(Message(
            role=role,
            content=content,
            metadata=metadata or {}
        ))
    
    def get_messages(self, limit: int = None) -> List[Message]:
        """获取消息"""
        if limit:
            return self.messages[-limit:]
        return self.messages
    
    def clear(self):
        """清空消息"""
        self.messages.clear()


@dataclass
class EmotionState:
    """情绪状态 - 统一接口"""
    # PAD 维度
    pleasure: float = 0.0      # 愉悦度 [-1, 1]
    arousal: float = 0.0       # 唤醒度 [-1, 1]
    dominance: float = 0.0   # 控制度 [-1, 1]
    
    # 神经递质
    dopamine: float = 0.5      # 多巴胺 [0, 1]
    cortisol: float = 0.3     # 皮质醇 [0, 1]
    
    # OCC 情绪
    dominant_emotion: str = ""   # 主导情绪
    emotion_intensity: float = 0.0  # 情绪强度
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pleasure": self.pleasure,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "dopamine": self.dopamine,
            "cortisol": self.cortisol,
            "dominant_emotion": self.dominant_emotion,
            "emotion_intensity": self.emotion_intensity
        }
    
    @staticmethod
    def from_dict(d: Dict) -> 'EmotionState':
        return EmotionState(
            pleasure=d.get("pleasure", 0.0),
            arousal=d.get("arousal", 0.0),
            dominance=d.get("dominance", 0.0),
            dopamine=d.get("dopamine", 0.5),
            cortisol=d.get("cortisol", 0.3),
            dominant_emotion=d.get("dominant_emotion", ""),
            emotion_intensity=d.get("emotion_intensity", 0.0)
        )


@dataclass
class Response:
    """响应"""
    content: str
    emotion: EmotionState = field(default_factory=EmotionState)
    actions: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "emotion": self.emotion.to_dict(),
            "actions": self.actions,
            "metadata": self.metadata
        }


@dataclass
class AppConfig:
    """应用配置"""
    # LLM
    llm_provider: str = "mock"
    llm_model: str = ""
    llm_api_key: str = ""
    llm_base_url: str = ""
    
    # 情感
    emotion_model: str = "occ"  # "occ" 或 "pad"
    
    # 人格
    personality: str = "default"
    
    # 病理
    pathology: str = "none"
    
    # 记忆
    memory_enabled: bool = True
    
    # Web
    web_host: str = "0.0.0.0"
    web_port: int = 8001
    
    def to_dict(self) -> Dict:
        return {
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "emotion_model": self.emotion_model,
            "personality": self.personality,
            "pathology": self.pathology,
            "memory_enabled": self.memory_enabled
        }
    
    @staticmethod
    def from_dict(d: Dict) -> 'AppConfig':
        config = AppConfig()
        for k, v in d.items():
            if hasattr(config, k):
                setattr(config, k, v)
        return config
