"""
动作事件数据模型

定义运动皮层输出的动作类型和事件结构
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import json


class ActionType(Enum):
    """
    动作类型枚举
    
    定义运动皮层可以执行的所有动作类型
    """
    TYPING = "typing"           # 显示正在输入状态
    MESSAGE = "message"         # 发送消息内容
    WAIT = "wait"               # 等待/停顿
    THINKING = "thinking"       # 思考状态（可选扩展）


@dataclass
class ActionEvent:
    """
    动作事件
    
    表示运动皮层输出的一个原子动作，包含动作类型、内容和持续时间
    
    Attributes:
        action_type: 动作类型
        content: 动作内容（如消息文本）
        duration: 持续时间（秒）
        metadata: 额外的元数据（如情绪状态、调试信息等）
    """
    action_type: ActionType
    content: str = ""
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        
        Returns:
            Dict[str, Any]: 字典格式的动作事件
        """
        return {
            "action": self.action_type.value,
            "content": self.content,
            "duration": self.duration,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """
        转换为 JSON 格式
        
        Returns:
            str: JSON 格式的动作事件
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActionEvent":
        """
        从字典创建动作事件
        
        Args:
            data: 字典格式的动作事件
            
        Returns:
            ActionEvent: 动作事件实例
        """
        action_type = ActionType(data["action"])
        return cls(
            action_type=action_type,
            content=data.get("content", ""),
            duration=data.get("duration", 0.0),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def create_typing(cls, duration: float, metadata: Optional[Dict[str, Any]] = None) -> "ActionEvent":
        """
        创建正在输入动作
        
        Args:
            duration: 输入持续时间
            metadata: 元数据
            
        Returns:
            ActionEvent: 正在输入动作事件
        """
        return cls(
            action_type=ActionType.TYPING,
            duration=duration,
            metadata=metadata or {}
        )
    
    @classmethod
    def create_message(cls, content: str, metadata: Optional[Dict[str, Any]] = None) -> "ActionEvent":
        """
        创建发送消息动作
        
        Args:
            content: 消息内容
            metadata: 元数据
            
        Returns:
            ActionEvent: 发送消息动作事件
        """
        return cls(
            action_type=ActionType.MESSAGE,
            content=content,
            metadata=metadata or {}
        )
    
    @classmethod
    def create_wait(cls, duration: float, metadata: Optional[Dict[str, Any]] = None) -> "ActionEvent":
        """
        创建等待动作
        
        Args:
            duration: 等待持续时间
            metadata: 元数据
            
        Returns:
            ActionEvent: 等待动作事件
        """
        return cls(
            action_type=ActionType.WAIT,
            duration=duration,
            metadata=metadata or {}
        )
