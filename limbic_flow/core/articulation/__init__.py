"""
运动皮层模块 (Motor Cortex / Articulation Core)

生物学对应：运动皮层 (Motor Cortex) & 布若卡氏区 (Broca's Area)
功能定位：输出节奏控制与分段发送引擎

核心职责：
- 将 LLM 生成的"语义块"解耦为"时间流"
- 模拟真人的打字速度、犹豫感、断句习惯
- 情绪状态直接影响打字速度和发送频率

架构位置：LLM 表现层之后，最终输出接口之前
"""

from .motor_cortex import MotorCortex
from .action_event import ActionEvent, ActionType
from .streaming_integration import (
    ArticulationStreamingOutput,
    ArticulationExecutor,
    create_articulation_executor
)

__all__ = [
    "MotorCortex",
    "ActionEvent",
    "ActionType",
    "ArticulationStreamingOutput",
    "ArticulationExecutor",
    "create_articulation_executor"
]
