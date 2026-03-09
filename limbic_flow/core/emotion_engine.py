"""
情绪引擎 - PAD 与神经递质、半衰期衰减的独立实现

[说明]
这是简化版的情绪引擎，适用于:
- 独立脚本
- 文档示例
- 非 Pipeline 场景

对于完整的 Pipeline 使用，建议直接使用 Amygdala 类。
"""

import time
from typing import Dict, Any, Optional
from limbic_flow.core.config import LimbicConfig, HalfLifeConfig, BaselineConfig
from limbic_flow.core.amygdala.decay import DecayCalculator, EmotionalState


class EmotionEngine:
    """
    情绪引擎 - 独立使用的情绪状态管理器
    
    [比喻] 就像一个简单的"心情记录器":
    - 记录当前心情
    - 随时间自动衰减
    - 响应新的刺激
    
    [使用场景]
    - 简单的情绪追踪脚本
    - 文档和示例
    - 不需要持久化的场景
    
    [注意]
    Pipeline 中完整的情绪处理请使用 Amygdala 类
    """

    def __init__(
        self, 
        config: LimbicConfig = None,
        decay_calculator: DecayCalculator = None
    ):
        """
        初始化情绪引擎
        
        Args:
            config: 配置对象（可选，默认使用全局配置）
            decay_calculator: 衰减计算器（可选）
        """
        # 加载配置
        self.config = config or LimbicConfig()
        self.baseline = self.config.baseline
        
        # 初始化衰减计算器
        self.decay_calculator = decay_calculator or DecayCalculator(
            self.config.half_life
        )
        
        # 初始状态 - 从基线开始
        self.state = EmotionalState(
            pleasure=self.baseline.pleasure,
            arousal=self.baseline.arousal,
            dominance=self.baseline.dominance,
            dopamine=self.baseline.dopamine,
            cortisol=self.baseline.cortisol,
        )
        
        # 上次更新时间戳
        self.last_update_time = time.time()

    def feel(
        self, 
        pleasure: float = 0.0, 
        arousal: float = 0.0, 
        dominance: float = 0.0
    ) -> Dict[str, float]:
        """
        感受情绪刺激 - 主要入口方法
        
        [比喻] 就像人感受到某件事:
        - 好消息 → pleasure=0.5
        - 惊吓 → arousal=0.8, dominance=-0.3
        - 掌控感 → dominance=0.5
        
        Args:
            pleasure: 愉悦度变化 [-1, 1]
            arousal: 唤醒度变化 [-1, 1]
            dominance: 控制度变化 [-1, 1]
        
        Returns:
            更新后的情绪状态
        """
        # 1. 先应用时间衰减
        self._apply_time_decay()
        
        # 2. 叠加新的刺激
        self.state = self.decay_calculator.apply_stimulus(
            self.state, pleasure, arousal, dominance
        )
        
        # 3. 更新神经递质
        self.state = self.decay_calculator.update_neurotransmitters(self.state)
        
        # 4. 更新时间戳
        self.last_update_time = time.time()
        
        return self.get_state()

    def _apply_time_decay(self) -> None:
        """应用时间衰减"""
        current_time = time.time()
        time_delta = current_time - self.last_update_time
        
        if time_delta > 0:
            self.state = self.decay_calculator.decay_state(
                self.state, 
                time_delta,
                self.baseline
            )
            self.last_update_time = current_time

    def relax(self, amount: float = 0.2) -> Dict[str, float]:
        """
        放松 - 降低唤醒度和压力
        
        [比喻] 就像深呼吸一口气，平静下来
        
        Args:
            amount: 放松程度 [0, 1]
        
        Returns:
            更新后的状态
        """
        return self.feel(
            pleasure=amount * 0.1,      # 轻微愉悦
            arousal=-amount * 0.5,    # 降低唤醒度
            dominance=amount * 0.2     # 轻微增加控制感
        )

    def stress(self, amount: float = 0.3) -> Dict[str, float]:
        """
        紧张 - 增加压力和唤醒度
        
        [比喻] 就像遇到威胁时紧张起来
        
        Args:
            amount: 紧张程度 [0, 1]
        
        Returns:
            更新后的状态
        """
        return self.feel(
            pleasure=-amount * 0.3,    # 不愉悦
            arousal=amount * 0.8,      # 高唤醒
            dominance=-amount * 0.5    # 失去控制感
        )

    def reward(self, amount: float = 0.3) -> Dict[str, float]:
        """
        奖励 - 感到开心和满足
        
        [比喻] 就像收到好消息或奖励
        
        Args:
            amount: 愉悦程度 [0, 1]
        
        Returns:
            更新后的状态
        """
        return self.feel(
            pleasure=amount * 0.8,     # 愉悦
            arousal=amount * 0.3,      # 轻微兴奋
            dominance=amount * 0.2     # 轻微掌控感
        )

    def get_state(self) -> Dict[str, float]:
        """
        获取当前情绪状态
        
        Returns:
            情绪状态字典
        """
        # 先应用一次衰减，确保状态是最新的
        self._apply_time_decay()
        
        return {
            "pleasure": self.state.pleasure,
            "arousal": self.state.arousal,
            "dominance": self.state.dominance,
            "dopamine": self.state.dopamine,
            "cortisol": self.state.cortisol,
            "timestamp": self.last_update_time
        }
    
    def get_mood_description(self) -> str:
        """
        获取心情描述 - 更人性化的表达
        
        Returns:
            描述当前心情的文字
        """
        state = self.get_state()
        
        # 基于 PAD 值生成描述
        descriptions = []
        
        # 愉悦度
        if state["pleasure"] > 0.5:
            descriptions.append("开心")
        elif state["pleasure"] > 0.2:
            descriptions.append("愉快")
        elif state["pleasure"] < -0.5:
            descriptions.append("沮丧")
        elif state["pleasure"] < -0.2:
            descriptions.append("郁闷")
        
        # 唤醒度
        if state["arousal"] > 0.5:
            descriptions.append("兴奋")
        elif state["arousal"] > 0.2:
            descriptions.append("警觉")
        elif state["arousal"] < -0.5:
            descriptions.append("困倦")
        elif state["arousal"] < -0.2:
            descriptions.append("平静")
        
        # 控制感
        if state["dominance"] > 0.3:
            descriptions.append("自信")
        elif state["dominance"] < -0.3:
            descriptions.append("无助")
        
        # 神经递质补充
        if state["dopamine"] > 0.7:
            descriptions.append("充满期待")
        if state["cortisol"] > 0.7:
            descriptions.append("压力山大")
        
        if not descriptions:
            return "平静"
        
        return " · ".join(descriptions)

    def reset(self) -> None:
        """重置到基线状态"""
        self.state = EmotionalState(
            pleasure=self.baseline.pleasure,
            arousal=self.baseline.arousal,
            dominance=self.baseline.dominance,
            dopamine=self.baseline.dopamine,
            cortisol=self.baseline.cortisol,
        )
        self.last_update_time = time.time()


# 便捷函数
def create_relaxed_engine() -> EmotionEngine:
    """创建放松型情绪引擎（情绪稳定，衰减慢）"""
    return EmotionEngine(config=LimbicConfig.relaxed())


def create_sensitive_engine() -> EmotionEngine:
    """创建敏感型情绪引擎（情绪波动大，衰减快）"""
    return EmotionEngine(config=LimbicConfig.sensitive())
