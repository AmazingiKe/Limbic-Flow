"""
运动皮层与流式输出的集成

提供将 ActionEvent 流转换为可执行的流式输出的能力
"""

import time
from typing import List, Callable, Optional, Dict, Any
from .action_event import ActionEvent, ActionType
from ..streaming import StreamingOutput
from ...utils.logger import get_logger


class ArticulationStreamingOutput(StreamingOutput):
    """
    运动皮层流式输出实现
    
    将 ActionEvent 流转换为带有时间节奏的输出
    """
    
    def __init__(
        self,
        action_callback: Callable[[ActionEvent], None],
        enable_timing: bool = True,
        enable_logging: bool = False
    ):
        """
        初始化运动皮层流式输出
        
        Args:
            action_callback: 动作回调函数，接收 ActionEvent
            enable_timing: 是否启用时间控制（模拟打字速度和停顿）
            enable_logging: 是否启用日志输出
        """
        self.logger = get_logger("ArticulationStreamingOutput")
        self.action_callback = action_callback
        self.enable_timing = enable_timing
        self.enable_logging = enable_logging
        self.buffer = ""
    
    def write(self, content: str) -> None:
        """
        写入内容（此方法在 Articulation 模式中不使用）
        
        Args:
            content: 要写入的内容
        """
        # 在 Articulation 模式下，我们不直接写入内容
        # 而是通过 execute_actions 方法执行动作流
        pass
    
    def flush(self) -> None:
        """
        刷新缓冲区
        """
        if self.buffer:
            self.action_callback(ActionEvent.create_message(self.buffer))
            self.buffer = ""
    
    def close(self) -> None:
        """
        关闭输出
        """
        self.flush()
    
    def execute_actions(self, actions: List[ActionEvent]) -> None:
        """
        执行动作流
        
        Args:
            actions: 动作事件列表
        """
        for action in actions:
            # 执行动作
            self._execute_action(action)
            
            # 如果启用时间控制，则等待
            if self.enable_timing and action.duration > 0:
                time.sleep(action.duration)
    
    def _execute_action(self, action: ActionEvent) -> None:
        """
        执行单个动作
        
        Args:
            action: 动作事件
        """
        if self.enable_logging:
            self.logger.debug(f"[Articulation] {action.action_type.value}: {action.content[:50] if action.content else ''} (duration: {action.duration:.2f}s)")
        
        # 调用回调函数
        self.action_callback(action)


class ArticulationExecutor:
    """
    运动皮层执行器
    
    负责协调 MotorCortex 和 StreamingOutput，实现完整的表达流程
    """
    
    def __init__(
        self,
        action_callback: Callable[[ActionEvent], None],
        enable_timing: bool = True,
        enable_logging: bool = False
    ):
        """
        初始化运动皮层执行器
        
        Args:
            action_callback: 动作回调函数，接收 ActionEvent
            enable_timing: 是否启用时间控制
            enable_logging: 是否启用日志输出
        """
        self.output = ArticulationStreamingOutput(
            action_callback=action_callback,
            enable_timing=enable_timing,
            enable_logging=enable_logging
        )
    
    def execute(
        self,
        actions: List[ActionEvent],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        执行动作流
        
        Args:
            actions: 动作事件列表
            metadata: 额外的元数据
        """
        try:
            self.output.execute_actions(actions)
        finally:
            self.output.close()
    
    def execute_with_callback(
        self,
        actions: List[ActionEvent],
        callback: Callable[[ActionEvent], None],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        使用自定义回调执行动作流
        
        Args:
            actions: 动作事件列表
            callback: 自定义回调函数
            metadata: 额外的元数据
        """
        original_callback = self.output.action_callback
        self.output.action_callback = callback
        
        try:
            self.output.execute_actions(actions)
        finally:
            self.output.action_callback = original_callback
            self.output.close()


def create_articulation_executor(
    action_callback: Callable[[ActionEvent], None],
    enable_timing: bool = True,
    enable_logging: bool = False
) -> ArticulationExecutor:
    """
    创建运动皮层执行器的便捷函数
    
    Args:
        action_callback: 动作回调函数
        enable_timing: 是否启用时间控制
        enable_logging: 是否启用日志输出
        
    Returns:
        ArticulationExecutor: 运动皮层执行器实例
    """
    return ArticulationExecutor(
        action_callback=action_callback,
        enable_timing=enable_timing,
        enable_logging=enable_logging
    )
