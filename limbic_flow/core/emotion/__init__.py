"""
情感模块

包含:
- OCC: OCC 认知情绪模型
  - OCCEmotion: 22种情绪类型
  - OCCState: 情绪状态
  - OCCEngine: 认知评估引擎
  - OCCHalfLifeConfig: 差异化半衰期
  - OCCToPADProjector: OCC→PAD 投影
- Appraiser: LLM 驱动的认知评估
- StateManager: 情绪状态管理
  - EmotionState: 完整情绪状态 (PAD + 神经递质 + 调节)
  - EmotionStateManager: 状态管理器
  - NeurotransmitterState: 神经递质状态
  - RegulationState: 调节状态
"""

from limbic_flow.core.emotion.occ import (
    OCCEngine, 
    OCCState, 
    OCCEmotion, 
    create_occ_engine,
    OCCHalfLifeConfig,
    OCCToPADProjector
)
from limbic_flow.core.emotion.appraiser import LLMAppraiser, create_appraiser
from limbic_flow.core.emotion.state_manager import (
    EmotionState,
    EmotionStateManager,
    Neurotransmitter,
    NeurotransmitterState,
    RegulationState,
    create_state_manager,
)

__all__ = [
    # OCC
    "OCCEngine",
    "OCCState", 
    "OCCEmotion",
    "create_occ_engine",
    "OCCHalfLifeConfig",
    "OCCToPADProjector",
    # Appraiser
    "LLMAppraiser",
    "create_appraiser",
    # State Manager
    "EmotionState",
    "EmotionStateManager",
    "Neurotransmitter",
    "NeurotransmitterState",
    "RegulationState",
    "create_state_manager",
]
