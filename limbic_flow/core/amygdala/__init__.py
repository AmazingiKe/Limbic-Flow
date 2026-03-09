"""
杏仁核 - 情绪中心与神经递质调节器

[职责] 情绪处理的核心模块:
- 接收外界刺激，计算情绪反应
- 管理情绪记忆的存储和检索
- 计算神经递质水平（多巴胺、皮质醇）
- 应用时间衰减

[设计原则]
- 配置驱动：通过 LimbicConfig 调整行为
- 依赖注入：存储层和计算器可替换
- 单一职责：各组件各司其职
"""

import time
from typing import List, Dict, Any, Optional
from limbic_flow.core.config import LimbicConfig, ThresholdConfig, BaselineConfig
from limbic_flow.core.types import CognitiveState
from limbic_flow.core.amygdala.storage import MemoryStore, SQLiteMemoryStore, EmotionalMemory
from limbic_flow.core.amygdala.decay import DecayCalculator, EmotionalState


class Amygdala:
    """
    杏仁核 - 情绪处理中心
    
    [比喻] 就像人的情绪中枢:
    - 听到好消息 → 开心（愉悦度上升）
    - 遇到威胁 → 紧张（唤醒度上升，控制感下降）
    - 持续压力 → 焦虑（皮质醇累积）
    - 受到奖励 → 期待（多巴胺上升）
    
    [可替换性] 
    - 存储层可替换（SQLite → Redis → 内存）
    - 衰减计算器可替换（不同衰减模型）
    - 配置可定制（敏感型 vs 放松型）
    """

    def __init__(
        self, 
        config: LimbicConfig = None,
        storage: MemoryStore = None,
        decay_calculator: DecayCalculator = None
    ):
        """
        初始化杏仁核
        
        Args:
            config: 情绪系统配置
            storage: 记忆存储层（默认使用 SQLite）
            decay_calculator: 衰减计算器（默认使用标准模型）
        """
        self.config = config or LimbicConfig()
        self.storage = storage or SQLiteMemoryStore(self.config.database_path)
        self.decay_calculator = decay_calculator or DecayCalculator(self.config.half_life)
        self.threshold = self.config.threshold
        self.baseline = self.config.baseline

    def process(self, state: CognitiveState) -> CognitiveState:
        """
        处理情绪反应 - 核心方法
        
        流程:
        1. 获取上一时刻的情绪状态
        2. 应用时间衰减
        3. 叠加本轮刺激
        4. 计算神经递质
        5. 记录到记忆
        
        Args:
            state: 包含用户输入和当前PAD的认知状态
            
        Returns:
            更新后的认知状态（包含神经递质）
        """
        # 1. 获取历史状态并计算衰减
        baseline_state = self._calculate_baseline(state.timestamp)
        
        # 2. 叠加新的情绪刺激
        current_state = self._apply_stimulus(
            baseline_state,
            state.pad_vector.get("pleasure", 0.0),
            state.pad_vector.get("arousal", 0.0),
            state.pad_vector.get("dominance", 0.0)
        )
        
        # 3. 计算神经递质
        neurotransmitters = self._compute_neurotransmitters(
            current_state,
            state.environmental_pressure
        )
        
        # 4. 更新状态
        state.pad_vector = current_state.to_dict()
        state.neurotransmitters = neurotransmitters
        
        # 5. 记录到记忆
        self._record_state(state)
        
        return state
    
    def _calculate_baseline(self, current_time: float) -> EmotionalState:
        """
        计算当前时刻的情绪基线
        
        从记忆库获取上一时刻状态，应用时间衰减
        
        Args:
            current_time: 当前时间戳
            
        Returns:
            衰减后的情绪状态
        """
        latest = self.storage.get_latest()
        
        if latest is None:
            # 首次运行，返回默认基线
            return EmotionalState(
                pleasure=self.baseline.pleasure,
                arousal=self.baseline.arousal,
                dominance=self.baseline.dominance,
                dopamine=self.baseline.dopamine,
                cortisol=self.baseline.cortisol,
            )
        
        # 计算时间差
        time_delta = max(0.0, current_time - latest.timestamp)
        
        # 应用衰减
        return self.decay_calculator.decay_state(
            EmotionalState.from_dict(latest.to_dict()),
            time_delta,
            self.baseline
        )
    
    def _apply_stimulus(
        self, 
        base_state: EmotionalState,
        pleasure: float,
        arousal: float,
        dominance: float
    ) -> EmotionalState:
        """
        叠加情绪刺激
        
        Args:
            base_state: 基础状态
            pleasure: 愉悦度输入
            arousal: 唤醒度输入
            dominance: 控制度输入
            
        Returns:
            叠加刺激后的状态
        """
        return EmotionalState(
            pleasure=max(-1.0, min(1.0, base_state.pleasure + pleasure)),
            arousal=max(-1.0, min(1.0, base_state.arousal + arousal)),
            dominance=max(-1.0, min(1.0, base_state.dominance + dominance)),
            dopamine=base_state.dopamine,
            cortisol=base_state.cortisol,
        )
    
    def _compute_neurotransmitters(
        self, 
        state: EmotionalState,
        environmental_pressure: float = 0.0
    ) -> Dict[str, float]:
        """
        计算神经递质水平
        
        根据当前情绪状态和环境压力计算:
        - 皮质醇（压力激素）
        - 多巴胺（奖励激素）
        
        Args:
            state: 当前情绪状态
            environmental_pressure: 环境压力
            
        Returns:
            神经递质水平
        """
        # 1. 计算累积压力
        cumulative_stress = self._calculate_cumulative_stress()
        
        # 2. 计算当前压力
        current_stress = self._calculate_current_stress(
            state.arousal,
            state.dominance
        )
        
        # 3. 计算皮质醇
        base_cortisol = state.cortisol
        cortisol = base_cortisol + cumulative_stress + current_stress + environmental_pressure
        cortisol = max(0.0, min(1.0, cortisol))
        
        # 4. 计算多巴胺
        base_dopamine = state.dopamine
        dopamine_boost = 0.0
        
        if state.pleasure > self.threshold.reward_pleasure:
            dopamine_boost += 0.2
        if state.dominance > self.threshold.reward_dominance:
            dopamine_boost += 0.1
            
        dopamine = base_dopamine + dopamine_boost
        dopamine = max(0.0, min(1.0, dopamine))
        
        return {
            "dopamine": dopamine,
            "cortisol": cortisol,
        }
    
    def _calculate_cumulative_stress(self) -> float:
        """
        计算累积压力
        
        分析最近的情绪历史，检测是否有持续的负面情绪模式
        
        Returns:
            累积压力值 [0, 1]
        """
        recent = self.storage.get_recent(limit=self.threshold.stress_window)
        
        if not recent:
            return 0.0
        
        cumulative = 0.0
        for record in recent:
            # 高唤醒 + 低愉悦 = 压力
            if (record.arousal > self.threshold.stress_history_threshold and 
                record.pleasure < self.threshold.stress_history_pleasure):
                cumulative += 0.1
        
        return cumulative
    
    def _calculate_current_stress(
        self, 
        arousal: float, 
        dominance: float
    ) -> float:
        """
        计算当前压力
        
        基于当前的唤醒度和控制感
        
        Args:
            arousal: 当前唤醒度
            dominance: 当前控制感
            
        Returns:
            当前压力值 [0, 1]
        """
        if (arousal > self.threshold.stress_arousal and 
            dominance < self.threshold.stress_dominance):
            return 0.2
        return 0.0
    
    def _record_state(self, state: CognitiveState) -> None:
        """
        记录状态到记忆库
        
        Args:
            state: 要记录的状态
        """
        memory = EmotionalMemory(
            timestamp=state.timestamp,
            pleasure=state.pad_vector.get("pleasure", 0.0),
            arousal=state.pad_vector.get("arousal", 0.0),
            dominance=state.pad_vector.get("dominance", 0.0),
            dopamine=state.neurotransmitters.get("dopamine", 0.5),
            cortisol=state.neurotransmitters.get("cortisol", 0.3),
            context=state.user_input
        )
        self.storage.save(memory)
    
    def get_emotional_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取情绪历史
        
        方便调试和可视化
        
        Args:
            limit: 返回记录数
            
        Returns:
            情绪历史列表
        """
        memories = self.storage.get_recent(limit=limit)
        return [m.to_dict() for m in memories]
    
    def get_current_state(self) -> EmotionalState:
        """
        获取当前情绪状态
        
        Returns:
            当前的 EmotionalState
        """
        latest = self.storage.get_latest()
        if latest is None:
            return EmotionalState(
                pleasure=self.baseline.pleasure,
                arousal=self.baseline.arousal,
                dominance=self.baseline.dominance,
                dopamine=self.baseline.dopamine,
                cortisol=self.baseline.cortisol,
            )
        return EmotionalState.from_dict(latest.to_dict())
    
    def reset(self) -> None:
        """重置杏仁核状态（清空记忆）"""
        # 重新初始化存储
        self.storage = SQLiteMemoryStore(self.config.database_path)
    
    def close(self) -> None:
        """关闭连接"""
        self.storage.close()


# 便捷函数 - 使用默认配置创建杏仁核
_default_amygdala = None

def get_default_amygdala() -> Amygdala:
    """获取默认的杏仁核实例"""
    global _default_amygdala
    if _default_amygdala is None:
        _default_amygdala = Amygdala()
    return _default_amygdala
