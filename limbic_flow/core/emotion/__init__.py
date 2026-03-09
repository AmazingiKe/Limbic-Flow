"""
情感模块

包含:
- OCC: OCC 认知情绪模型
- PAD: PAD 维度情绪模型 (兼容)
"""

from limbic_flow.core.emotion.occ import OCCEngine, OCCState, OCCEmotion, create_occ_engine

__all__ = [
    "OCCEngine",
    "OCCState", 
    "OCCEmotion",
    "create_occ_engine",
]
