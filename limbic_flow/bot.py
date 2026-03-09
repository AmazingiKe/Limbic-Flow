"""
Limbic-Flow 高级 API - 简化的入口

[用途]
- 一行代码创建 bot
- 预设场景快速启动
- 简洁的对话接口
"""

from typing import Dict, Any, Optional, List, Generator
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.pipeline.config import PipelineConfig
from limbic_flow.core.amygdala import Amygdala
from limbic_flow.core.config import LimbicConfig
from limbic_flow.utils.event_bus import get_event_bus, Event, EventType


class LimbicBot:
    """
    Limbic-Flow 机器人 - 高级 API
    
    [用途] 简化的对话接口，适合快速开发
    
    [Example]
    >>> bot = LimbicBot.sensitive()
    >>> response = bot.chat("你好！")
    >>> print(response)
    """
    
    def __init__(self, pipeline: LimbicFlowPipeline):
        self.pipeline = pipeline
        self.event_bus = get_event_bus()
    
    @classmethod
    def create(
        cls,
        mode: str = "default",
        llm_provider: str = None,
        **kwargs
    ) -> "LimbicBot":
        """
        创建机器人
        
        Args:
            mode: 模式 - "default", "relaxed", "sensitive", "alzheimer"
            llm_provider: LLM 提供商
            **kwargs: 其他配置
        
        Returns:
            LimbicBot 实例
        """
        # 选择预设配置
        if mode == "relaxed":
            config = PipelineConfig.relaxed()
        elif mode == "sensitive":
            config = PipelineConfig.sensitive()
        elif mode == "alzheimer":
            config = PipelineConfig.alzheimer_mode()
        else:
            config = PipelineConfig()
        
        # 覆盖配置
        if llm_provider:
            config.llm_provider = llm_provider
        
        # 创建 pipeline
        pipeline = LimbicFlowPipeline(config=config)
        
        return cls(pipeline)
    
    @classmethod
    def default(cls, **kwargs) -> "LimbicBot":
        """默认模式"""
        return cls.create("default", **kwargs)
    
    @classmethod
    def relaxed(cls, **kwargs) -> "LimbicBot":
        """放松模式"""
        return cls.create("relaxed", **kwargs)
    
    @classmethod
    def sensitive(cls, **kwargs) -> "LimbicBot":
        """敏感模式"""
        return cls.create("sensitive", **kwargs)
    
    @classmethod
    def alzheimer(cls, **kwargs) -> "LimbicBot":
        """阿尔茨海默模式"""
        return cls.create("alzheimer", **kwargs)
    
    def chat(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        对话（同步）
        
        Args:
            message: 用户消息
            context: 上下文
        
        Returns:
            机器人回复
        """
        # 发布开始事件
        self.event_bus.publish(Event(
            type=EventType.PIPELINE_START,
            data={"message": message}
        ))
        
        # 处理输入
        actions = list(self.pipeline.process_input_stream(message, context))
        
        # 提取文本
        text = ""
        for action in actions:
            if action.action_type.value == "speak":
                text += action.content
        
        # 发布结束事件
        self.event_bus.publish(Event(
            type=EventType.PIPELINE_END,
            data={"response": text}
        ))
        
        return text
    
    def chat_stream(self, message: str, context: Dict[str, Any] = None) -> Generator[str, None, None]:
        """
        对话（流式）
        
        Args:
            message: 用户消息
            context: 上下文
        
        Yields:
            片段文本
        """
        for action in self.pipeline.process_input_stream(message, context):
            if action.action_type.value == "speak":
                yield action.content
    
    def get_emotion(self) -> Dict[str, Any]:
        """
        获取当前情绪状态
        
        Returns:
            情绪状态字典
        """
        state = self.pipeline.amygdala.get_current_state()
        return state.to_dict()
    
    def reset_emotion(self) -> None:
        """重置情绪"""
        self.pipeline.amygdala.reset()
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        config = self.pipeline.config
        return {
            "mode": "sensitive" if config.use_sensitive_emotion else "default",
            "llm_provider": config.llm_provider,
            "pathologies": {
                "depression": config.enable_depression,
                "alzheimer": config.enable_alzheimer,
                "ptsd": config.enable_ptsd,
                "hsp": config.enable_hsp,
            }
        }


# 便捷函数
def create_bot(mode: str = "default", **kwargs) -> LimbicBot:
    """创建机器人"""
    return LimbicBot.create(mode, **kwargs)
