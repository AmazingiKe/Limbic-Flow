"""
元认知系统 - 基于研究文档实现

参考:
- METACOGNITION_CONSCIOUSNESS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import math
import time
import random


class UncertaintyType(Enum):
    """不确定性类型"""
    ALEATORIC = "aleatoric"       # 随机不确定性 (固有)
    EPISTEMIC = "epistemic"       # 认知不确定性 (可减少)
    MODEL = "model"               # 模型不确定性
    DECISION = "decision"         # 决策不确定性


@dataclass
class UncertaintyMetrics:
    """不确定性指标"""
    aleatoric: float = 0.0
    epistemic: float = 0.0
    model: float = 0.0
    decision: float = 0.0
    
    def total(self) -> float:
        return (self.aleatoric + self.epistemic + self.model + self.decision) / 4
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "aleatoric": self.aleatoric,
            "epistemic": self.epistemic,
            "model": self.model,
            "decision": self.decision,
            "total": self.total()
        }


@dataclass
class MetacognitiveState:
    """元认知状态"""
    confidence: float = 0.8          # 置信度 [0-1]
    uncertainty: UncertaintyMetrics = field(default_factory=UncertaintyMetrics)
    self_monitor_score: float = 0.5  # 自我监控能力
    reflection_count: int = 0         # 反思次数
    last_reflection: float = 0.0     # 上次反思时间


class SelfMonitor:
    """
    自我监控系统
    
    研究: 监控自己的思维过程
    - 前思考钩子 (pre-thinking)
    - 中思考钩子 (during-thinking)  
    - 后思考钩子 (post-thinking)
    """
    
    def __init__(self):
        self.hooks = {
            "pre_thinking": [],
            "during_thinking": [],
            "post_thinking": []
        }
        self.state = MetacognitiveState()
        
        # 监控参数
        self.reflection_interval = 60  # 每60秒反思一次
    
    def register_hook(self, stage: str, callback: Callable):
        """注册钩子"""
        if stage in self.hooks:
            self.hooks[stage].append(callback)
    
    def pre_thinking(self, context: Dict) -> Dict:
        """前思考钩子"""
        # 执行所有前思考钩子
        for hook in self.hooks["pre_thinking"]:
            context = hook(context)
        
        # 更新状态
        self.state.reflection_count += 1
        self.state.last_reflection = time.time()
        
        return context
    
    def during_thinking(self, context: Dict, thought: str) -> Dict:
        """中思考钩子 - 实时监控"""
        # 检查是否需要干预
        if self._should_intervene(thought):
            context["intervention"] = self._generate_intervention(thought)
        
        for hook in self.hooks["during_thinking"]:
            thought = hook(thought)
        
        return context
    
    def post_thinking(self, context: Dict, result: Dict) -> Dict:
        """后思考钩子 - 评估结果"""
        # 评估置信度
        self._update_confidence(result)
        
        for hook in self.hooks["post_thinking"]:
            result = hook(result)
        
        return result
    
    def _should_intervene(self, thought: str) -> bool:
        """判断是否需要干预"""
        # 检测到不确定或错误的模式
        uncertain_patterns = ["可能", "也许", "不确定", "不知道"]
        
        for pattern in uncertain_patterns:
            if pattern in thought:
                return True
        
        return False
    
    def _generate_intervention(self, thought: str) -> str:
        """生成干预建议"""
        interventions = [
            "让我再仔细想想...",
            "我需要更多上下文",
            "这个结论可能需要验证",
            "让我换个角度思考"
        ]
        return random.choice(interventions)
    
    def _update_confidence(self, result: Dict):
        """更新置信度"""
        # 基于结果准确性更新
        # 简化: 随机波动
        delta = random.uniform(-0.1, 0.1)
        self.state.confidence = max(0.0, min(1.0, self.state.confidence + delta))


class ConfidenceCalibrator:
    """
    置信度校准
    
    研究: 确保置信度与实际准确性匹配
    - 直方图分箱校准
    - ECE (Expected Calibration Error)
    """
    
    def __init__(self, n_bins: int = 10):
        self.n_bins = n_bins
        self.bin_confidences = [[] for _ in range(n_bins)]
        self.bin_accuracies = [[] for _ in range(n_bins)]
    
    def record(self, confidence: float, is_correct: bool):
        """记录置信度和结果"""
        bin_idx = min(int(confidence * self.n_bins), self.n_bins - 1)
        
        self.bin_confidences[bin_idx].append(confidence)
        self.bin_accuracies[bin_idx].append(1.0 if is_correct else 0.0)
    
    def calculate_ece(self) -> float:
        """计算期望校准误差 (ECE)"""
        total_samples = 0
        ece = 0.0
        
        for i in range(self.n_bins):
            samples = len(self.bin_accuracies[i])
            if samples == 0:
                continue
            
            avg_confidence = sum(self.bin_confidences[i]) / samples
            avg_accuracy = sum(self.bin_accuracies[i]) / samples
            
            ece += (samples / sum(len(b) for b in self.bin_accuracies)) * abs(avg_confidence - avg_accuracy)
            total_samples += samples
        
        return ece
    
    def calibrate(self, confidence: float) -> float:
        """校准置信度"""
        bin_idx = min(int(confidence * self.n_bins), self.n_bins - 1)
        
        if len(self.bin_accuracies[bin_idx]) > 0:
            # 使用该区间的实际准确率
            calibrated = sum(self.bin_accuracies[bin_idx]) / len(self.bin_accuracies[bin_idx])
            # 与原始置信度混合
            return confidence * 0.7 + calibrated * 0.3
        
        return confidence


class UncertaintyQuantifier:
    """
    不确定性量化
    
    研究:
    -  aleatoric: 固有随机性
    - epistemic: 知识不足
    - 模型不确定性
    - 决策不确定性
    """
    
    def __init__(self):
        self.knowledge_gaps: Dict[str, float] = {}
    
    def quantify(
        self,
        context: Dict,
        model_outputs: List[Dict],
        decision_options: List[str]
    ) -> UncertaintyMetrics:
        """量化各类型不确定性"""
        
        # Aleatoric - 基于输出的多样性
        aleatoric = self._calculate_aleatoric(model_outputs)
        
        # Epistemic - 基于知识缺口
        epistemic = self._calculate_epistemic(context)
        
        # Model - 基于模型一致性
        model = self._calculate_model_uncertainty(model_outputs)
        
        # Decision - 基于选项相似度
        decision = self._calculate_decision_uncertainty(decision_options)
        
        return UncertaintyMetrics(
            aleatoric=aleatoric,
            epistemic=epistemic,
            model=model,
            decision=decision
        )
    
    def _calculate_aleatoric(self, outputs: List[Dict]) -> float:
        """计算 aleatoric 不确定性"""
        if len(outputs) < 2:
            return 0.0
        
        # 基于输出分布的熵
        confidences = [o.get("confidence", 0.5) for o in outputs]
        
        # 计算方差
        mean = sum(confidences) / len(confidences)
        variance = sum((c - mean) ** 2 for c in confidences) / len(confidences)
        
        return min(1.0, variance * 4)  # 缩放到 [0,1]
    
    def _calculate_epistemic(self, context: Dict) -> float:
        """计算 epistemic 不确定性"""
        # 基于上下文中的知识缺口
        uncertainty = 0.0
        
        # 检查关键信息缺失
        if not context.get("has_context"):
            uncertainty += 0.3
        if not context.get("has_history"):
            uncertainty += 0.2
        if not context.get("has_domain_knowledge"):
            uncertainty += 0.4
        
        return min(1.0, uncertainty)
    
    def _calculate_model_uncertainty(self, outputs: List[Dict]) -> float:
        """计算模型不确定性"""
        if len(outputs) < 2:
            return 0.0
        
        # 基于输出不一致
        outputs_str = [str(o) for o in outputs]
        unique_outputs = len(set(outputs_str))
        
        return min(1.0, unique_outputs / len(outputs))
    
    def _calculate_decision_uncertainty(self, options: List[str]) -> float:
        """计算决策不确定性"""
        if len(options) <= 1:
            return 0.0
        
        # 简化为选项数量相关
        # 更多选项 = 更高不确定性
        return min(1.0, (len(options) - 1) * 0.1)


class MetacognitionEngine:
    """
    元认知引擎
    
    整合自我监控、置信度校准、不确定性量化
    """
    
    def __init__(self):
        self.monitor = SelfMonitor()
        self.calibrator = ConfidenceCalibrator()
        self.quantifier = UncertaintyQuantifier()
        self.state = MetacognitiveState()
    
    def think(
        self,
        input_context: Dict,
        thinking_process: Callable
    ) -> Dict:
        """
        元认知思考流程
        
        Args:
            input_context: 输入上下文
            thinking_process: 思考过程函数
        
        Returns:
            Dict: 包含结果和元认知信息
        """
        # 1. 前思考
        context = self.monitor.pre_thinking(input_context)
        
        # 2. 执行思考
        result = thinking_process(context)
        
        # 3. 中思考
        context = self.monitor.during_thinking(context, result.get("thought", ""))
        
        # 4. 后思考 + 不确定性量化
        context = self.monitor.post_thinking(context, result)
        
        # 5. 量化不确定性
        uncertainty = self.quantifier.quantify(
            context,
            result.get("model_outputs", []),
            result.get("options", [])
        )
        
        # 6. 更新状态
        self.state.uncertainty = uncertainty
        self.state.confidence = self.calibrator.calibrate(self.state.confidence)
        
        return {
            "result": result,
            "metacognition": {
                "confidence": self.state.confidence,
                "uncertainty": uncertainty.to_dict(),
                "reflection_count": self.state.reflection_count
            }
        }
    
    def reflect(self, content: str, evaluation: str) -> Dict:
        """
        反思
        
        研究: 反思自己的思维过程
        """
        self.state.reflection_count += 1
        self.state.last_reflection = time.time()
        
        # 更新自我监控能力
        if "good" in evaluation.lower() or "correct" in evaluation.lower():
            self.state.self_monitor_score = min(1.0, self.state.self_monitor_score + 0.05)
        else:
            self.state.self_monitor_score = max(0.0, self.state.self_monitor_score - 0.02)
        
        return {
            "reflection_id": self.state.reflection_count,
            "content": content,
            "evaluation": evaluation,
            "self_monitor_score": self.state.self_monitor_score
        }


# 示例
if __name__ == "__main__":
    engine = MetacognitionEngine()
    
    # 定义思考过程
    def thinking_process(ctx):
        return {
            "thought": "这是一个测试思考",
            "result": "测试结果",
            "confidence": 0.7,
            "model_outputs": [
                {"text": "结果1", "confidence": 0.7},
                {"text": "结果2", "confidence": 0.65}
            ],
            "options": ["选项A", "选项B", "选项C"]
        }
    
    # 执行
    result = engine.think({"input": "test"}, thinking_process)
    
    print(f"Confidence: {result['metacognition']['confidence']}")
    print(f"Uncertainty: {result['metacognition']['uncertainty']}")
