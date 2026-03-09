"""
认知模块 - 认知功能实现

包含:
- 元认知
- 预测处理
- 睡眠与梦
"""

from .metacognition import (
    MetacognitionEngine,
    SelfMonitor,
    ConfidenceCalibrator,
    UncertaintyQuantifier,
    MetacognitiveState,
    UncertaintyMetrics,
    UncertaintyType,
)

from .predictive import (
    PredictiveProcessor,
    FreeEnergyCalculator,
    ActiveInference,
    PredictiveCodingNetwork,
    Prediction,
    PredictionError,
    PredictionLevel,
)

__all__ = [
    # Metacognition
    "MetacognitionEngine",
    "SelfMonitor",
    "ConfidenceCalibrator",
    "UncertaintyQuantifier",
    "MetacognitiveState",
    "UncertaintyMetrics",
    "UncertaintyType",
    # Predictive Processing
    "PredictiveProcessor",
    "FreeEnergyCalculator",
    "ActiveInference",
    "PredictiveCodingNetwork",
    "Prediction",
    "PredictionError",
    "PredictionLevel",
]
