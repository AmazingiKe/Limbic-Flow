"""
好奇心与探索系统 - 基于研究文档实现

参考:
- CURIOSITY_EXPLORATION.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math
import random
import numpy as np


class CuriosityType(Enum):
    """好奇心类型"""
    PERCEPTUAL = "perceptual"     # 感知好奇心
    EPISTEMIC = "epistemic"       # 认知好奇心
    DIVERSIVE = "diversive"      # 广泛好奇心
    SPECIFIC = "specific"         # 特定好奇心
    SOCIAL = "social"             # 社会好奇心


@dataclass
class CuriosityState:
    """好奇心状态"""
    current_type: CuriosityType = CuriosityType.DIVERSIVE
    intensity: float = 0.5        # 好奇心强度
    information_gap: float = 0.0   # 信息缺口
    novelty_bonus: float = 0.0    # 新奇度奖励


class CuriositySystem:
    """
    好奇心系统
    
    研究: 内在动机驱动的探索行为
    - 信息缺口理论
    - 新奇检测
    - 信息增益
    """
    
    def __init__(self):
        self.state = CuriosityState()
        
        # 参数
        self.novelty_sensitivity = 0.7    # 新奇敏感度
        self.habituation_rate = 0.3       # 习惯化速率
        self.max_novelty_bonus = 0.5      # 最大新奇奖励
        self.information_gain_weight = 0.4 # 信息增益权重
        
        # 记忆: 已曝光的刺激
        self.exposure_memory: Dict[str, int] = {}
    
    def calculate_curiosity_drive(
        self, 
        stimulus: Dict,
        available_energy: float = 1.0
    ) -> float:
        """
        计算好奇心驱动力
        
        CuriosityDrive = information_gap × uncertainty × available_energy
        """
        # 计算信息缺口
        information_gap = self._calculate_information_gap(stimulus)
        
        # 计算不确定性
        uncertainty = self._calculate_uncertainty(stimulus)
        
        # 新奇度
        novelty = self._calculate_novelty_reward(stimulus)
        
        # 综合驱动力
        drive = information_gap * uncertainty * available_energy + novelty
        
        # 更新状态
        self.state.information_gap = information_gap
        self.state.novelty_bonus = novelty
        self.state.intensity = min(1.0, drive)
        
        return drive
    
    def _calculate_information_gap(self, stimulus: Dict) -> float:
        """计算信息缺口"""
        # 简化为: 未知特征的比例
        known_features = stimulus.get("known_features", [])
        unknown_features = stimulus.get("unknown_features", [])
        
        if not unknown_features:
            return 0.0
        
        total = len(known_features) + len(unknown_features)
        return len(unknown_features) / total if total > 0 else 0.0
    
    def _calculate_uncertainty(self, stimulus: Dict) -> float:
        """计算不确定性"""
        # 基于预测概率的熵
        predictions = stimulus.get("predictions", [0.5])
        
        # 计算熵
        entropy = 0.0
        for p in predictions:
            if p > 0 and p < 1:
                entropy -= p * math.log2(p) + (1-p) * math.log2(1-p)
        
        # 归一化
        max_entropy = math.log2(len(predictions)) if predictions else 1
        return entropy / max_entropy if max_entropy > 0 else 0.5
    
    def _calculate_novelty_reward(self, stimulus: Dict) -> float:
        """计算新奇奖励"""
        signature = stimulus.get("signature", str(random.random()))
        
        # 曝光次数
        exposure = self.exposure_memory.get(signature, 0)
        
        # 更新曝光记忆
        self.exposure_memory[signature] = exposure + 1
        
        # 新奇度衰减
        if exposure == 0:
            return self.max_novelty_bonus
        else:
            # 递减回报
            novelty = self.max_novelty_bonus / (1 + exposure * self.habituation_rate)
            return novelty * self.novelty_sensitivity
    
    def select_curiosity_type(self, context: Dict) -> CuriosityType:
        """根据上下文选择好奇心类型"""
        # 检测环境特征
        is_novel = context.get("is_novel", False)
        is_social = context.get("is_social", False)
        has_information_gap = context.get("has_information_gap", False)
        
        if is_social:
            return CuriosityType.SOCIAL
        elif has_information_gap:
            return CuriosityType.EPISTEMIC
        elif is_novel:
            return CuriosityType.DIVERSIVE
        else:
            return CuriosityType.PERCEPTUAL


class InformationGainCalculator:
    """
    信息增益计算器
    
    好奇心可以框架为信息增益(减少不确定性)
    """
    
    def __init__(self):
        self.prior_uncertainty = 0.5
        self.learning_rate = 0.1
    
    def calculate_information_gain(
        self,
        prior_distribution: List[float],
        posterior_distribution: List[float]
    ) -> float:
        """
        计算信息增益
        
        InformationGain = H(before) - H(after)
        """
        prior_entropy = self._entropy(prior_distribution)
        posterior_entropy = self._entropy(posterior_distribution)
        
        return max(0, prior_entropy - posterior_entropy)
    
    def _entropy(self, distribution: List[float]) -> float:
        """计算香农熵"""
        entropy = 0.0
        for p in distribution:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def expected_information_gain(
        self,
        possible_outcomes: List[Dict]
    ) -> float:
        """计算期望信息增益"""
        total_eig = 0.0
        
        for outcome in possible_outcomes:
            probability = outcome.get("probability", 0.1)
            information_gain = outcome.get("information_gain", 0.0)
            
            total_eig += probability * information_gain
        
        return total_eig


class ExplorationExploitation:
    """
    探索-利用权衡
    
    研究: ε-greedy, UCB, Thompson Sampling
    """
    
    def __init__(self, strategy: str = "ucb"):
        self.strategy = strategy
        
        # 参数
        self.epsilon = 0.1          # ε-greedy 参数
        self.exploration_constant = 2.0  # UCB 探索常数
        self.alpha = 0.1           # 学习率
        
        # 记忆
        self.action_values: Dict[str, float] = {}
        self.action_counts: Dict[str, int] = {}
    
    def select_action(
        self,
        actions: List[str],
        context: Optional[Dict] = None
    ) -> str:
        """
        选择动作
        
        Returns:
            str: 选择的动作
        """
        if self.strategy == "epsilon_greedy":
            return self._epsilon_greedy(actions)
        elif self.strategy == "ucb":
            return self._ucb(actions)
        elif self.strategy == "thompson":
            return self._thompson_sampling(actions)
        else:
            return actions[0] if actions else ""
    
    def _epsilon_greedy(self, actions: List[str]) -> str:
        """ε-greedy 算法"""
        if random.random() < self.epsilon:
            # 探索: 随机选择
            return random.choice(actions)
        else:
            # 利用: 选择已知最佳
            return self._get_best_action(actions)
    
    def _ucb(self, actions: List[str]) -> str:
        """Upper Confidence Bound 算法"""
        total_counts = sum(self.action_counts.values()) if self.action_counts else 1
        
        best_action = actions[0]
        best_value = float('-inf')
        
        for action in actions:
            # 初始化
            if action not in self.action_values:
                self.action_values[action] = 0.0
                self.action_counts[action] = 0
            
            value = self.action_values[action]
            count = self.action_counts[action]
            
            # UCB 公式
            if count == 0:
                ucb_value = float('inf')
            else:
                ucb_value = value + self.exploration_constant * math.sqrt(
                    math.log(total_counts) / count
                )
            
            if ucb_value > best_value:
                best_value = ucb_value
                best_action = action
        
        return best_action
    
    def _thompson_sampling(self, actions: List[str]) -> str:
        """Thompson Sampling 算法"""
        samples = {}
        
        for action in actions:
            if action not in self.action_values:
                self.action_values[action] = 0.5
                self.action_counts[action] = 0
            
            # 从 Beta 分布采样
            alpha = self.action_values[action] * 10 + 1
            beta = (1 - self.action_values[action]) * 10 + 1
            
            samples[action] = np.random.beta(alpha, beta)
        
        # 选择采样值最大的
        return max(samples, key=samples.get)
    
    def _get_best_action(self, actions: List[str]) -> str:
        """获取已知最佳动作"""
        best = actions[0]
        best_value = float('-inf')
        
        for action in actions:
            value = self.action_values.get(action, 0.0)
            if value > best_value:
                best_value = value
                best = action
        
        return best
    
    def update(self, action: str, reward: float):
        """更新动作价值"""
        if action not in self.action_values:
            self.action_values[action] = 0.0
            self.action_counts[action] = 0
        
        # 更新计数
        self.action_counts[action] += 1
        count = self.action_counts[action]
        
        # 增量更新值
        value = self.action_values[action]
        self.action_values[action] = value + self.alpha * (reward - value)


class EnergyManagement:
    """
    能量管理系统
    
    研究:
    - 代谢模拟
    - 认知疲劳
    - 能量感知调度
    """
    
    def __init__(self):
        self.current_energy = 1.0       # 当前能量 [0-1]
        self.max_energy = 1.0
        self.recovery_rate = 0.01       # 恢复速率
        self.consumption_rate = 0.02     # 消耗速率
        
        # 疲劳累积
        self.fatigue = 0.0
        self.fatigue_threshold = 0.8
    
    def consume(self, amount: float):
        """消耗能量"""
        self.current_energy = max(0, self.current_energy - amount)
        self.fatigue = min(1.0, self.fatigue + amount * 0.5)
    
    def recover(self, amount: float = None):
        """恢复能量"""
        if amount is None:
            amount = self.recovery_rate
        
        self.current_energy = min(self.max_energy, self.current_energy + amount)
        
        # 疲劳恢复较慢
        if self.current_energy > 0.5:
            self.fatigue = max(0, self.fatigue - amount * 0.2)
    
    def should_explore(self) -> bool:
        """判断是否应该探索"""
        # 能量低或疲劳高时减少探索
        if self.fatigue > self.fatigue_threshold:
            return False
        
        if self.current_energy < 0.3:
            return False
        
        return True
    
    def get_exploration_budget(self) -> float:
        """获取探索预算"""
        # 基于能量和疲劳计算探索预算
        energy_factor = self.current_energy
        fatigue_factor = 1.0 - self.fatigue
        
        return min(1.0, energy_factor * fatigue_factor)


class CuriosityEngine:
    """
    好奇心引擎
    
    整合好奇心、探索-利用权衡、能量管理
    """
    
    def __init__(self):
        self.curiosity = CuriositySystem()
        self.exploration = ExplorationExploitation(strategy="ucb")
        self.energy = EnergyManagement()
        self.info_gain = InformationGainCalculator()
    
    def think(
        self,
        context: Dict,
        available_actions: List[str]
    ) -> Dict:
        """
        思考过程
        
        Returns:
            Dict: 包含决策信息
        """
        # 1. 检查能量
        if not self.energy.should_explore():
            # 能量不足,利用已知最佳
            action = self.exploration._get_best_action(available_actions)
            return {
                "action": action,
                "mode": "exploit",
                "reason": "low_energy"
            }
        
        # 2. 计算好奇心驱动
        curiosity_drive = self.curiosity.calculate_curiosity_drive(context)
        
        # 3. 选择动作
        if curiosity_drive > 0.5 and random.random() < curiosity_drive:
            # 高好奇心,选择探索
            action = self.exploration.select_action(available_actions, context)
            mode = "explore"
        else:
            # 低好奇心,利用
            action = self.exploration._get_best_action(available_actions)
            mode = "exploit"
        
        # 4. 消耗能量
        energy_cost = 0.02 if mode == "explore" else 0.01
        self.energy.consume(energy_cost)
        
        return {
            "action": action,
            "mode": mode,
            "curiosity_drive": curiosity_drive,
            "energy": self.energy.current_energy,
            "fatigue": self.energy.fatigue
        }
    
    def update(self, action: str, reward: float):
        """更新学习"""
        # 更新探索-利用策略
        self.exploration.update(action, reward)
        
        # 能量恢复
        self.energy.recover()


# 示例
if __name__ == "__main__":
    engine = CuriosityEngine()
    
    # 模拟决策
    context = {
        "is_novel": True,
        "has_information_gap": True,
        "predictions": [0.3, 0.7],
        "signature": "stim_001"
    }
    
    actions = ["action_a", "action_b", "action_c"]
    
    result = engine.think(context, actions)
    print(f"Action: {result['action']}, Mode: {result['mode']}")
    print(f"Curiosity drive: {result['curiosity_drive']:.2f}")
    print(f"Energy: {result['energy']:.2f}")
