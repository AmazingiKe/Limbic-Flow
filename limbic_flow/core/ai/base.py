from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class MessageRole(Enum):
    """消息角色枚举"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """消息数据类"""
    role: MessageRole
    content: str

    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {"role": self.role.value, "content": self.content}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Message":
        """从字典创建消息"""
        return cls(role=MessageRole(data["role"]), content=data["content"])


@dataclass
class LLMResponse:
    """LLM 响应数据类"""
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class LLMConfig:
    """LLM 配置数据类"""
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: int = 30
    extra_params: Optional[Dict[str, Any]] = None


class BaseLLM(ABC):
    """
    LLM 抽象基类
    
    设计原则：
    - 依赖倒置：高层模块依赖此抽象接口，不依赖具体实现
    - 开闭原则：新增LLM只需继承此类，无需修改现有代码
    - 单一职责：每个适配器只负责一个厂商的API对接
    
    使用场景：
    - 作为 Limbic-Flow 的抽象层，支持多种 LLM 提供商
    - 支持运行时切换不同的 LLM 提供商
    - 统一的接口调用，降低学习成本
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 LLM
        
        Args:
            config: LLM 配置
        """
        self.config = config
        self._initialize_client()

    @abstractmethod
    def _initialize_client(self):
        """
        初始化 LLM 客户端
        
        子类必须实现此方法，用于初始化具体的 API 客户端
        """
        pass

    @abstractmethod
    def chat(
        self,
        messages: List[Union[Message, Dict[str, str]]],
        **kwargs
    ) -> LLMResponse:
        """
        聊天接口 - 核心方法
        
        Args:
            messages: 消息列表，可以是 Message 对象或字典
            **kwargs: 额外的参数，会覆盖 config 中的参数
        
        Returns:
            LLMResponse: LLM 响应对象
        
        Raises:
            Exception: 调用失败时抛出异常
        """
        pass

    def chat_simple(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        简化的聊天接口 - 单轮对话
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            **kwargs: 额外的参数
        
        Returns:
            LLMResponse: LLM 响应对象
        """
        messages = []
        
        if system_prompt:
            messages.append(Message(role=MessageRole.SYSTEM, content=system_prompt))
        
        messages.append(Message(role=MessageRole.USER, content=prompt))
        
        return self.chat(messages, **kwargs)

    def _normalize_messages(
        self,
        messages: List[Union[Message, Dict[str, str]]]
    ) -> List[Dict[str, str]]:
        """
        标准化消息格式
        
        Args:
            messages: 原始消息列表
        
        Returns:
            List[Dict[str, str]]: 标准化后的消息列表
        """
        normalized = []
        for msg in messages:
            if isinstance(msg, Message):
                normalized.append(msg.to_dict())
            elif isinstance(msg, dict):
                normalized.append(msg)
            else:
                raise ValueError(f"不支持的消息类型: {type(msg)}")
        return normalized

    def _merge_config(self, **kwargs) -> Dict[str, Any]:
        """
        合并配置，kwargs 中的参数优先级更高
        
        Args:
            **kwargs: 额外的参数
        
        Returns:
            Dict[str, Any]: 合并后的配置
        """
        merged = {
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "timeout": self.config.timeout,
        }
        
        if self.config.extra_params:
            merged.update(self.config.extra_params)
        
        merged.update(kwargs)
        
        return merged

    def get_model_name(self) -> str:
        """
        获取当前使用的模型名称
        
        Returns:
            str: 模型名称
        """
        return self.config.model

    def health_check(self) -> bool:
        """
        健康检查 - 验证 LLM 是否可用
        
        Returns:
            bool: 是否可用
        """
        try:
            response = self.chat_simple("ping", max_tokens=5)
            return bool(response.content)
        except Exception:
            return False
