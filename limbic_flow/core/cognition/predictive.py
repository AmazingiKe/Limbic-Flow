"""
预测处理系统 - 基于研究文档实现

参考:
- PREDICTIVE_PROCESSING.md
- 自由能原理 (Free Energy Principle)
- 主动推理 (Active Inference)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import math
import numpy as np


class PredictionLevel(Enum):
    """预测层级"""
    LOW = "low"       # 低级 (感官输入)
    MID = "mid"       # 中级 (对象)
    HIGH = "high"     # 高级 (情境)


@dataclass
class Prediction:
    """预测结构"""
    level: PredictionLevel
    content: str
    probability: float  # 预测置信度
    precision: float    # 精度 (对不确定性的加权)
    timestamp: float


@dataclass
class PredictionError:
    """预测误差"""
    level: PredictionLevel
    expected: any
    actual: any
    surprise: float     # 惊异度
    kl_divergence: float  # KL散度


class PredictiveProcessor:
    """
    预测处理核心
    
    研究参考:
    - 层级预测编码
    - 自由能最小化
    - 精度加权
    """
    
    def __init__(self):
        self.hierarchy_levels = {
            PredictionLevel.LOW: [],
            PredictionLevel.MID: [],
            PredictionLevel.HIGH: []
        }
        
        # 参数
        self.learning_rate = 0.1
        self.precision_weight = 0.5  # 精度权重
        self.surprise_threshold = 0.7  # 惊异阈值
    
    def predict(self, context: Dict) -> List[Prediction]:
        """
        生成预测
        
        Args:
            context: 当前上下文
        
        Returns:
            List[Prediction]: 预测列表
        """
        predictions = []
        
        # 从高层到低层生成预测
        for level in [PredictionLevel.HIGH, PredictionLevel.MID, PredictionLevel.LOW]:
            level_predictions = self._generate_level_predictions(level, context)
            predictions.extend(level_predictions)
        
        return predictions
    
    def _generate_level_predictions(self, level: PredictionLevel, context: Dict) -> List[Prediction]:
        """生成特定层级的预测"""
        predictions = []
        
        if level == PredictionLevel.HIGH:
            # 高级预测 - 情境
            predictions.append(Prediction(
                level=level,
                content="情境预测",
                probability=0.8,
                precision=0.6,
                timestamp=0
            ))
        
        elif level == PredictionLevel.MID:
            # 中级预测 - 对象
            predictions.append(Prediction(
                level=level,
                content="对象预测",
                probability=0.75,
                precision=0.7,
                timestamp=0
            ))
        
        else:
            # 低级预测 - 感官
            predictions.append(Prediction(
                level=level,
                content="感官预测",
                probability=0.7,
                precision=0.8,
                timestamp=0
            ))
        
        return predictions
    
    def compute_prediction_error(
        self, 
        prediction: Prediction, 
        actual: any
    ) -> PredictionError:
        """
        计算预测误差
        
        研究: 预测误差 = 实际 - 预测
        """
        # 计算惊异度 (surprise)
        if prediction.probability > 0:
            surprise = -math.log(prediction.probability)
        else:
            surprise = float('inf')
        
        # 归一化到 [0, 1]
        surprise = min(1.0, surprise / 10)
        
        # 计算 KL 散度
        kl = self._compute_kl(prediction.probability, actual)
        
        return PredictionError(
            level=prediction.level,
            expected=prediction.content,
            actual=actual,
            surprise=surprise,
            kl_divergence=kl
        )
    
    def _compute_kl(self, p: float, q: any) -> float:
        """计算简化的 KL 散度"""
        # 简化: 使用惊异度作为代理
        return abs(p - (1.0 if q else 0.0))
    
    def update_predictions(
        self, 
        errors: List[PredictionError]
    ) -> None:
        """
        根据预测误差更新模型
        
        研究: 预测误差驱动学习
        """
        for error in errors:
            # 惊异度高 -> 更新预测模型
            if error.surprise > self.surprise_threshold:
                # 学习率 * 惊异度
                learning = self.learning_rate * error.surprise
                
                # 更新对应层级的预测
                self._update_level_model(error.level, learning)
    
    def _update_level_model(self, level: PredictionLevel, learning: float):
        """更新特定层级的模型"""
        # 简化: 调整预测概率
        for pred in self.hierarchy_levels[level]:
            pred.probability = pred.probability * (1 - learning) + 0.5 * learning


class FreeEnergyCalculator:
    """
    自由能计算器
    
    研究: 自由能原理 (FEP)
    - 智能系统通过最小化自由能来维持稳态
    - 自由能 = 惊异度 + 复杂度
    """
    
    def __init__(self):
        self.complexity_weight = 0.3
    
    def calculate(
        self,
        surprise: float,
        complexity: float,
        accuracy: float
    ) -> float:
        """
        计算自由能
        
        Args:
            surprise: 惊异度
            complexity: 复杂度 (预测的复杂性)
            accuracy: 准确性
        
        Returns:
            float: 自由能 (越低越好)
        """
        # 自由能 = 惊异度 + 复杂度 - 准确性
        free_energy = (
            surprise * 0.5 +
            complexity * self.complexity_weight -
            accuracy * 0.3
        )
        
        return max(0.0, free_energy)
    
    def expected_free_energy(
        self,
        possible_outcomes: List[Dict],
        preferences: Dict
    ) -> float:
        """
        计算期望自由能
        
        用于主动推理中选择行动
        """
        total_efe = 0.0
        
        for outcome in possible_outcomes:
            # 获取该结果的概率和价值
            probability = outcome.get("probability", 0.5)
            value = outcome.get("value", 0.0)
            
            # 期望自由能 = -value + uncertainty
            efe = -value + (1 - probability)
            total_efe += efe * probability
        
        return total_efe


class ActiveInference:
    """
    主动推理
    
    研究:
    - 智能体主动选择能最小化期望自由能的行动
    - 感知-行动循环
    """
    
    def __init__(self):
        self.predictor = PredictiveProcessor()
        self.free_energy = FreeEnergyCalculator()
        
        # 当前信念
        self.beliefs: Dict = {}
    
    def infer(self, observation: Dict, available_actions: List[str]) -> str:
        """
        推理最佳行动
        
        Args:
            observation: 当前观察
            available_actions: 可用行动
        
        Returns:
            str: 最佳行动
        """
        # 1. 生成对每个行动的预测
        action_values = []
        
        for action in available_actions:
            # 模拟行动结果
            predicted_outcomes = self._simulate_action(action, observation)
            
            # 计算期望自由能
            efe = self.free_energy.expected_free_energy(
                predicted_outcomes,
                self.beliefs.get("preferences", {})
            )
            
            action_values.append((action, efe))
        
        # 2. 选择期望自由能最低的行动
        action_values.sort(key=lambda x: x[1])
        
        return action_values[0][0] if action_values else available_actions[0]
    
    def _simulate_action(self, action: str, observation: Dict) -> List[Dict]:
        """模拟行动结果"""
        # 简化: 返回预测结果
        return [
            {"probability": 0.7, "value": 0.8},
            {"probability": 0.3, "value": 0.4}
        ]
    
    def update_beliefs(self, observation: Dict, prediction_errors: List[PredictionError]):
        """更新信念"""
        # 基于预测误差更新信念
        for error in prediction_errors:
            # 信念更新
            if error.level in self.beliefs:
                # 简化: 信念向实际值调整
                self.beliefs[error.level] = (
                    self.beliefs[error.level] * 0.9 +
                    error.actual * 0.1
                )
            else:
                self.beliefs[error.level] = error.actual


class PredictiveCodingNetwork:
    """
    预测编码网络
    
    实现层级预测编码
    """
    
    def __init__(self, n_layers: int = 3):
        self.n_layers = n_layers
        
        # 每层的参数
        self.layers = [
            {
                "weights": np.random.rand(10, 10),
                "bias": np.zeros(10),
                "predictions": np.zeros(10),
                "errors": np.zeros(10)
            }
            for _ in range(n_layers)
        ]
    
    def forward(self, input_data: np.ndarray) -> List[np.ndarray]:
        """
        前向传播 - 生成预测
        
        Returns:
            List[np.ndarray]: 每层的预测
        """
        predictions = []
        current = input_data
        
        for i, layer in enumerate(self.layers):
            # 生成预测
            prediction = self._predict_layer(current, layer)
            predictions.append(prediction)
            
            # 传递到下一层
            current = prediction
        
        return predictions
    
    def _predict_layer(self, input_data: np.ndarray, layer: Dict) -> np.ndarray:
        """单层预测"""
        # 简化: 线性预测
        return np.dot(input_data, layer["weights"]) + layer["bias"]
    
    def backward(self, errors: List[np.ndarray]):
        """
        反向传播 - 更新模型
        
        研究: 预测误差自上而下传播
        """
        for i, layer in enumerate(self.layers):
            if i < len(errors):
                error = errors[i]
                
                # 更新权重
                # 简化: 使用误差更新
                layer["weights"] -= 0.01 * np.outer(error, error)
                layer["bias"] -= 0.01 * error


# 示例
if __name__ == "__main__":
    # 测试预测处理
    processor = PredictiveProcessor()
    predictions = processor.predict({"context": "test"})
    
    for pred in predictions:
        print(f"{pred.level.value}: {pred.content} (p={pred.probability})")
    
    # 测试主动推理
    inference = ActiveInference()
    best_action = inference.infer(
        {"observation": "test"},
        ["action1", "action2", "action3"]
    )
    print(f"\nBest action: {best_action}")
