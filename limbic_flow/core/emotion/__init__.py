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

__all__ = [
    "OCCEngine",
    "OCCState", 
    "OCCEmotion",
    "create_occ_engine",
    "OCCHalfLifeConfig",
    "OCCToPADProjector",
    "LLMAppraiser",
    "create_appraiser",
]
