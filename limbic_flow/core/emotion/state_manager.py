"""
情绪状态管理系统

[职责] 统一管理情感状态的完整生命周期
[设计] 整合 PAD、OCC、神经递质、调节策略
[可替换性] 状态持久化策略可替换

依赖:
- OCC 情绪模型 (limbic_flow.core.emotion.occ)
- 情绪调节引擎 (limbic_flow.core.emotion.regulation)
- 认知评估器 (limbic_flow.core.emotion.appraiser)

引用文档:
- docs/EMOTION_REGULATION_ALGORITHMS.md
- docs/STRESS_RESPONSE_SYSTEMS.md
- docs/DEVELOPMENTAL_EMOTIONAL_AI.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Literal, Callable
from enum import Enum
from datetime import datetime, timezone
import math
import json
import copy

# 导入现有模块
from limbic_flow.core.emotion.occ import (
    OCCEmotion,
    OCCState,
    OCCEngine,
    OCCToPADProjector,
    OCCHalfLifeConfig,
    Appraisal
)
from limbic_flow.core.emotion.regulation import (
    RegulationStrategy,
    RegulationResult,
    EmotionRegulationEngine
)


# ============================================================================
# 神经递质类型
# ============================================================================

class Neurotransmitter(Enum):
    """神经递质类型
    
    基于神经科学研究的主要神经递质:
    - 多巴胺: 奖励、动机、愉悦
    - 皮质醇: 压力、焦虑
    - 血清素: 情绪稳定、幸福感
    - 去甲肾上腺素: 唤醒、警觉
    - 内啡肽: 镇痛、愉悦
    """
    DOPAMINE = "dopamine"       # 多巴胺 - 奖励与动机
    CORTISOL = "cortisol"       # 皮质醇 - 压力激素
    SEROTONIN = "serotonin"     # 血清素 - 情绪稳定
    NOREPINEPHRINE = "norepinephrine"  # 去甲肾上腺素 - 警觉
    ENDORPHIN = "endorphin"     # 内啡肽 - 天然镇痛
    OXYTOCIN = "oxytocin"       # 催产素 - 社会联结
    GABA = "gaba"               # GABA - 抑制性神经递质
    GLUTAMATE = "glutamate"     # 谷氨酸 - 兴奋性神经递质


# ============================================================================
# 情绪状态类
# ============================================================================

@dataclass
class NeurotransmitterState:
    """神经递质状态
    
    模拟主要神经递质的动态水平 [0, 1]
    """
    dopamine: float = 0.5        # 多巴胺 - 奖励预期
    cortisol: float = 0.3        # 皮质醇 - 压力水平
    serotonin: float = 0.5       # 血清素 - 情绪稳定性
    norepinephrine: float = 0.4  # 去甲肾上腺素 - 警觉
    endorphin: float = 0.3      # 内啡肽 - 放松/愉悦
    oxytocin: float = 0.3        # 催产素 - 社交联结
    gaba: float = 0.5           # GABA - 抑制/平静
    glutamate: float = 0.4      # 谷氨酸 - 激活水平
    
    def to_dict(self) -> Dict[str, float]:
        """转换为字典"""
        return {
            "dopamine": self.dopamine,
            "cortisol": self.cortisol,
            "serotonin": self.serotonin,
            "norepinephrine": self.norepinephrine,
            "endorphin": self.endorphin,
            "oxytocin": self.oxytocin,
            "gaba": self.gaba,
            "glutamate": self.glutamate,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "NeurotransmitterState":
        """从字典创建"""
        return cls(
            dopamine=data.get("dopamine", 0.5),
            cortisol=data.get("cortisol", 0.3),
            serotonin=data.get("serotonin", 0.5),
            norepinephrine=data.get("norepinephrine", 0.4),
            endorphin=data.get("endorphin", 0.3),
            oxytocin=data.get("oxytocin", 0.3),
            gaba=data.get("gaba", 0.5),
            glutamate=data.get("glutamate", 0.4),
        )
    
    def clamp(self) -> "NeurotransmitterState":
        """限制所有值在 [0, 1] 范围内"""
        for key in self.__dict__:
            setattr(self, key, max(0.0, min(1.0, getattr(self, key))))
        return self


@dataclass
class RegulationState:
    """调节状态
    
    跟踪当前使用的调节策略及其效果
    """
    is_regulating: bool = False              # 是否正在调节
    strategy: Optional[str] = None            # 当前策略
    strategy_confidence: float = 0.0          # 策略置信度
    regulation_attempts: int = 0             # 调节尝试次数
    regulation_success: int = 0               # 调节成功次数
    last_regulation_time: Optional[datetime] = None
    regulation_history: List[Dict] = field(default_factory=list)
    
    def record_attempt(
        self, 
        strategy: str, 
        success: bool, 
        before_pad: Dict[str, float],
        after_pad: Dict[str, float]
    ):
        """记录调节尝试"""
        self.regulation_attempts += 1
        if success:
            self.regulation_success += 1
        
        self.regulation_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "strategy": strategy,
            "success": success,
            "confidence": self.strategy_confidence,
            "before_pad": before_pad,
            "after_pad": after_pad,
        })
        
        # 保持历史记录在合理长度
        if len(self.regulation_history) > 100:
            self.regulation_history = self.regulation_history[-50:]
    
    def get_success_rate(self) -> float:
        """获取调节成功率"""
        if self.regulation_attempts == 0:
            return 0.0
        return self.regulation_success / self.regulation_attempts


@dataclass
class EmotionState:
    """
    完整情绪状态
    
    整合 PAD、OCC、神经递质、调节状态的统一情绪表示
    
    属性:
        pad: PAD 三维度 (pleasure, arousal, dominance)
        neurotransmitters: 神经递质水平
        regulation: 调节状态
        timestamp: 状态时间戳
        occ_state: OCC 情绪状态
        source: 状态来源 (appraisal, detection, manual)
    """
    # PAD 维度
    pleasure: float = 0.0         # 愉悦度 [-1, 1]
    arousal: float = 0.0         # 唤醒度 [-1, 1]
    dominance: float = 0.0        # 掌控度 [-1, 1]
    
    # 神经递质
    neurotransmitters: NeurotransmitterState = field(
        default_factory=NeurotransmitterState
    )
    
    # 调节状态
    regulation: RegulationState = field(
        default_factory=RegulationState
    )
    
    # 元数据
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "init"                         # 状态来源
    context: str = ""                             # 上下文描述
    session_id: Optional[str] = None              # 会话 ID
    
    # OCC 状态
    occ_state: Optional[OCCState] = None
    
    # 原始/调节后状态
    original_pad: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        """初始化后处理"""
        self._clamp_values()
    
    def _clamp_values(self):
        """限制所有值在合法范围内"""
        self.pleasure = max(-1.0, min(1.0, self.pleasure))
        self.arousal = max(-1.0, min(1.0, self.arousal))
        self.dominance = max(-1.0, min(1.0, self.dominance))
        self.neurotransmitters.clamp()
    
    def to_pad_dict(self) -> Dict[str, float]:
        """转换为 PAD 字典"""
        return {
            "pleasure": self.pleasure,
            "arousal": self.arousal,
            "dominance": self.dominance,
        }
    
    @classmethod
    def from_pad_dict(cls, pad: Dict[str, float]) -> "EmotionState":
        """从 PAD 字典创建"""
        return cls(
            pleasure=pad.get("pleasure", 0.0),
            arousal=pad.get("arousal", 0.0),
            dominance=pad.get("dominance", 0.0),
        )
    
    def get_emotion_label(self) -> str:
        """获取情绪标签
        
        基于 PAD 值返回直观情绪标签
        """
        p, a, d = self.pleasure, self.arousal, self.dominance
        
        # 复合判断
        if p > 0.5 and a > 0.3:
            if d > 0.3:
                return "excited"      # 兴奋
            else:
                return "happy"       # 开心
        elif p < -0.5 and a > 0.3:
            if d < -0.3:
                return "angry"       # 愤怒
            else:
                return "afraid"      # 害怕
        elif p < -0.3:
            if a < 0:
                return "sad"         # 悲伤
            else:
                return "distressed"  # 苦恼
        elif a > 0.5:
            return "aroused"          # 警觉
        elif a < -0.3:
            return "calm"            # 平静
        elif d > 0.3:
            return "confident"       # 自信
        elif d < -0.3:
            return "submissive"      # 顺从
        else:
            return "neutral"         # 中性
    
    def get_intensity(self) -> float:
        """获取情绪强度
        
        综合 PAD 各维度的绝对值
        """
        return (abs(self.pleasure) + abs(self.arousal) + abs(self.dominance)) / 3
    
    def is_emotional(self, threshold: float = 0.3) -> bool:
        """判断是否有明显情绪反应"""
        return self.get_intensity() > threshold
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 (JSON 序列化)"""
        return {
            "pad": self.to_pad_dict(),
            "neurotransmitters": self.neurotransmitters.to_dict(),
            "regulation": {
                "is_regulating": self.regulation.is_regulating,
                "strategy": self.regulation.strategy,
                "attempts": self.regulation.regulation_attempts,
                "success_rate": self.regulation.get_success_rate(),
            },
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "context": self.context,
            "emotion_label": self.get_emotion_label(),
            "intensity": self.get_intensity(),
            "occ_state": self.occ_state.to_dict() if self.occ_state else None,
        }
    
    def to_json(self) -> str:
        """序列化为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmotionState":
        """从字典创建"""
        state = cls(
            pleasure=data.get("pad", {}).get("pleasure", 0.0),
            arousal=data.get("pad", {}).get("arousal", 0.0),
            dominance=data.get("pad", {}).get("dominance", 0.0),
            source=data.get("source", "restored"),
            context=data.get("context", ""),
        )
        
        # 恢复神经递质
        if "neurotransmitters" in data:
            state.neurotransmitters = NeurotransmitterState.from_dict(
                data["neurotransmitters"]
            )
        
        # 恢复时间戳
        if "timestamp" in data:
            state.timestamp = datetime.fromisoformat(data["timestamp"])
        
        return state
    
    def copy(self) -> "EmotionState":
        """深拷贝"""
        new_state = EmotionState(
            pleasure=self.pleasure,
            arousal=self.arousal,
            dominance=self.dominance,
            source=self.source,
            context=self.context,
            session_id=self.session_id,
            timestamp=datetime.now(timezone.utc),
        )
        new_state.neurotransmitters = copy.deepcopy(self.neurotransmitters)
        new_state.regulation = copy.deepcopy(self.regulation)
        if self.occ_state:
            new_state.occ_state = copy.deepcopy(self.occ_state)
        return new_state


# ============================================================================
# 情绪状态管理器
# ============================================================================

class EmotionStateManager:
    """
    情绪状态管理器
    
    [职责]
    - 跟踪情绪状态的完整生命周期
    - 处理情绪状态更新和转换
    - 管理情绪衰减
    - 协调 OCC 和 PAD 之间的转换
    - 集成调节策略
    
    [设计]
    - 使用事件驱动架构
    - 支持状态历史记录
    - 支持状态持久化回调
    """
    
    def __init__(
        self,
        decay_enabled: bool = True,
        default_half_life: float = 3600,
        auto_regulate: bool = True,
        regulation_threshold: float = 0.5,
    ):
        """
        初始化情绪状态管理器
        
        Args:
            decay_enabled: 是否启用情绪衰减
            default_half_life: 默认半衰期(秒)
            auto_regulate: 是否自动应用调节
            regulation_threshold: 自动调节阈值
        """
        # 当前状态
        self.current_state = EmotionState()
        
        # OCC 引擎
        self.occ_engine = OCCEngine()
        
        # 调节引擎
        self.regulation_engine = EmotionRegulationEngine()
        
        # 配置
        self.decay_enabled = decay_enabled
        self.default_half_life = default_half_life
        self.auto_regulate = auto_regulate
        self.regulation_threshold = regulation_threshold
        
        # 状态历史
        self.history: List[EmotionState] = []
        self.max_history_length = 1000
        
        # 事件回调
        self.on_state_change: List[Callable[[EmotionState, EmotionState], None]] = []
        self.on_regulation: List[Callable[[EmotionState, RegulationResult], None]] = []
        self.on_decay: List[Callable[[EmotionState, float], None]] = []
        
        # 统计
        self.state_change_count = 0
        self.decay_count = 0
        self.regulation_count = 0
        
        # OCC 半衰期配置
        self.occ_half_life_config = OCCHalfLifeConfig()
        
        # 持续时间跟踪
        self.last_update_time = datetime.now(timezone.utc)
        
        # 待处理的过渡
        self._pending_transition: Optional[EmotionState] = None
        self._transition_duration: float = 1.0
    
    # -------------------------------------------------------------------------
    # 状态更新
    # -------------------------------------------------------------------------
    
    def update_from_appraisal(
        self,
        appraisal: Appraisal,
        context: str = "",
        **kwargs
    ) -> EmotionState:
        """
        从认知评估更新状态
        
        Args:
            appraisal: OCC 认知评估结果
            context: 情境上下文
            **kwargs: 其他参数
        
        Returns:
            更新后的情绪状态
        """
        # 保存旧状态
        old_state = self.current_state.copy()
        
        # 通过 OCC 引擎处理
        occ_state = self.occ_engine.appraise(
            event={
                "type": "event",
                "desirability": appraisal.desirability,
                "likelihood": appraisal.likelihood,
                "expectedness": appraisal.expectedness,
                "goal_relevant": appraisal.goal_relevant,
                "realized": appraisal.realized,
            },
            context={"context": context}
        )
        
        # 投影到 PAD
        pad = OCCToPADProjector.project(occ_state)
        
        # 更新当前状态
        self.current_state.pleasure = pad["pleasure"]
        self.current_state.arousal = pad["arousal"]
        self.current_state.dominance = pad["dominance"]
        
        # 更新神经递质
        self._update_neurotransmitters_from_occ(occ_state)
        
        # 保存 OCC 状态
        self.current_state.occ_state = occ_state
        self.current_state.source = "appraisal"
        self.current_state.context = context
        
        # 更新时间
        self._update_timestamp()
        
        # 检查是否需要调节
        if self.auto_regulate:
            self._maybe_regulate(context)
        
        # 记录历史
        self._record_state(old_state)
        
        # 触发事件
        self._trigger_state_change(old_state, self.current_state)
        
        return self.current_state
    
    def update_from_pad(
        self,
        pad: Dict[str, float],
        source: str = "manual",
        context: str = "",
    ) -> EmotionState:
        """
        从 PAD 值直接更新状态
        
        Args:
            pad: PAD 字典
            source: 来源
            context: 上下文
        
        Returns:
            更新后的情绪状态
        """
        old_state = self.current_state.copy()
        
        # 直接更新 PAD
        self.current_state.pleasure = pad.get("pleasure", 0.0)
        self.current_state.arousal = pad.get("arousal", 0.0)
        self.current_state.dominance = pad.get("dominance", 0.0)
        
        # 推断神经递质
        self._infer_neurotransmitters_from_pad(pad)
        
        self.current_state.source = source
        self.current_state.context = context
        
        # 更新时间
        self._update_timestamp()
        
        # 检查调节
        if self.auto_regulate:
            self._maybe_regulate(context)
        
        # 记录历史
        self._record_state(old_state)
        
        # 触发事件
        self._trigger_state_change(old_state, self.current_state)
        
        return self.current_state
    
    def update_from_occ(
        self,
        occ_state: OCCState,
        source: str = "occ",
        context: str = "",
    ) -> EmotionState:
        """
        从 OCC 状态更新
        
        Args:
            occ_state: OCC 情绪状态
            source: 来源
            context: 上下文
        
        Returns:
            更新后的情绪状态
        """
        # 投影到 PAD
        pad = OCCToPADProjector.project(occ_state)
        
        # 更新神经递质
        self._update_neurotransmitters_from_occ(occ_state)
        
        # 调用 PAD 更新
        return self.update_from_pad(pad, source=source, context=context)
    
    def apply_stimulus(
        self,
        stimulus_type: str,
        intensity: float,
        context: str = "",
    ) -> EmotionState:
        """
        应用外部刺激
        
        Args:
            stimulus_type: 刺激类型 (positive, negative, neutral, arousal)
            intensity: 强度 [-1, 1]
            context: 上下文
        
        Returns:
            更新后的情绪状态
        """
        old_state = self.current_state.copy()
        
        if stimulus_type == "positive":
            self.current_state.pleasure = max(
                self.current_state.pleasure,
                intensity
            )
        elif stimulus_type == "negative":
            self.current_state.pleasure = min(
                self.current_state.pleasure,
                intensity
            )
        elif stimulus_type == "arousal":
            self.current_state.arousal = max(
                self.current_state.arousal,
                intensity
            )
        elif stimulus_type == "dominance":
            self.current_state.dominance = max(
                self.current_state.dominance,
                intensity
            )
        
        # 限制范围
        self.current_state._clamp_values()
        
        # 推断神经递质变化
        self._infer_neurotransmitters_from_pad(self.current_state.to_pad_dict())
        
        self.current_state.source = "stimulus"
        self.current_state.context = context
        
        # 更新时间
        self._update_timestamp()
        
        # 记录历史
        self._record_state(old_state)
        
        # 触发事件
        self._trigger_state_change(old_state, self.current_state)
        
        return self.current_state
    
    # -------------------------------------------------------------------------
    # 状态衰减
    # -------------------------------------------------------------------------
    
    def decay(self, time_delta: Optional[float] = None) -> EmotionState:
        """
        应用情绪衰减
        
        Args:
            time_delta: 经过的时间(秒)，如果为 None 则自动计算
        
        Returns:
            衰减后的状态
        """
        if not self.decay_enabled:
            return self.current_state
        
        # 计算时间增量
        if time_delta is None:
            now = datetime.now(timezone.utc)
            time_delta = (now - self.last_update_time).total_seconds()
        
        if time_delta <= 0:
            return self.current_state
        
        old_state = self.current_state.copy()
        
        # PAD 衰减
        decay_factor = math.exp(-math.log(2) * time_delta / self.default_half_life)
        
        self.current_state.pleasure *= decay_factor
        self.current_state.arousal *= decay_factor
        self.current_state.dominance *= decay_factor
        
        # 神经递质衰减 (回归基线)
        self._decay_neurotransmitters(time_delta)
        
        # OCC 状态衰减
        if self.current_state.occ_state:
            self.occ_engine.decay_differential(time_delta, self.occ_half_life_config)
            # 重新投影到 PAD
            pad = OCCToPADProjector.project(self.occ_engine.state)
            # 平滑混合
            self._blend_pad(pad, decay_factor)
        
        # 触发衰减事件
        self.decay_count += 1
        for callback in self.on_decay:
            callback(self.current_state, time_delta)
        
        # 更新时间
        self.last_update_time = datetime.now(timezone.utc)
        
        return self.current_state
    
    def _blend_pad(
        self, 
        new_pad: Dict[str, float], 
        weight: float = 0.5
    ):
        """混合新旧 PAD 值"""
        self.current_state.pleasure = (
            self.current_state.pleasure * (1 - weight) + 
            new_pad["pleasure"] * weight
        )
        self.current_state.arousal = (
            self.current_state.arousal * (1 - weight) + 
            new_pad["arousal"] * weight
        )
        self.current_state.dominance = (
            self.current_state.dominance * (1 - weight) + 
            new_pad["dominance"] * weight
        )
        self.current_state._clamp_values()
    
    # -------------------------------------------------------------------------
    # 情绪调节
    # -------------------------------------------------------------------------
    
    def regulate(
        self,
        context: str = "",
        strategy: Optional[RegulationStrategy] = None,
    ) -> RegulationResult:
        """
        应用情绪调节
        
        Args:
            context: 情境上下文
            strategy: 指定调节策略，如果为 None 则自动选择
        
        Returns:
            调节结果
        """
        old_state = self.current_state.copy()
        before_pad = self.current_state.to_pad_dict()
        
        # 应用调节
        result = self.regulation_engine.regulate(
            pad=before_pad,
            context=context,
            forced_strategy=strategy,
        )
        
        # 更新状态
        self.current_state.pleasure = result.regulated_pad["pleasure"]
        self.current_state.arousal = result.regulated_pad["arousal"]
        self.current_state.dominance = result.regulated_pad["dominance"]
        
        # 记录调节状态
        self.current_state.regulation.is_regulating = True
        self.current_state.regulation.strategy = result.strategy.value
        self.current_state.regulation.strategy_confidence = result.confidence
        self.current_state.regulation.last_regulation_time = datetime.now(timezone.utc)
        
        # 判断是否成功 (愉悦度改善)
        success = (
            result.regulated_pad["pleasure"] > before_pad["pleasure"] or
            result.regulated_pad["arousal"] < before_pad["arousal"]
        )
        
        self.current_state.regulation.record_attempt(
            strategy=result.strategy.value,
            success=success,
            before_pad=before_pad,
            after_pad=result.regulated_pad,
        )
        
        # 更新统计
        self.regulation_count += 1
        self.current_state.regulation.is_regulating = False
        
        # 触发事件
        for callback in self.on_regulation:
            callback(self.current_state, result)
        
        return result
    
    def _maybe_regulate(self, context: str):
        """检查是否需要自动调节"""
        intensity = self.current_state.get_intensity()
        
        # 高强度负面情绪需要调节
        if (self.current_state.pleasure < -0.4 and 
            intensity > self.regulation_threshold):
            self.regulate(context)
    
    # -------------------------------------------------------------------------
    # 神经递质更新
    # -------------------------------------------------------------------------
    
    def _update_neurotransmitters_from_occ(self, occ_state: OCCState):
        """从 OCC 状态更新神经递质"""
        # 使用 OCCToPADProjector 的方法
        nt_values = OCCToPADProjector.project_neurotransmitters(occ_state)
        
        # 更新多巴胺
        self.current_state.neurotransmitters.dopamine = nt_values["dopamine"]
        
        # 更新皮质醇
        self.current_state.neurotransmitters.cortisol = nt_values["cortisol"]
        
        # 根据 PAD 推断其他神经递质
        self._infer_other_neurotransmitters()
    
    def _infer_neurotransmitters_from_pad(self, pad: Dict[str, float]):
        """从 PAD 推断神经递质"""
        p, a, d = pad.get("pleasure", 0), pad.get("arousal", 0), pad.get("dominance", 0)
        
        # 多巴胺: 与愉悦度和掌控感正相关
        self.current_state.neurotransmitters.dopamine = (
            0.3 + p * 0.3 + d * 0.2
        )
        
        # 皮质醇: 与负面情绪和高唤醒相关
        self.current_state.neurotransmitters.cortisol = (
            0.3 - p * 0.3 + max(0, a) * 0.3
        )
        
        # 血清素: 与情绪稳定性正相关
        self.current_state.neurotransmitters.serotonin = (
            0.5 + (1 - abs(p)) * 0.2 - abs(a) * 0.1
        )
        
        # 去甲肾上腺素: 与唤醒度正相关
        self.current_state.neurotransmitters.norepinephrine = (
            0.3 + max(0, a) * 0.4
        )
        
        # GABA: 与平静状态正相关
        self.current_state.neurotransmitters.gaba = (
            0.5 - max(0, a) * 0.3 + min(0, a) * 0.2
        )
        
        # 限制范围
        self.current_state.neurotransmitters.clamp()
    
    def _infer_other_neurotransmitters(self):
        """推断其他神经递质 (基于已有的)"""
        nt = self.current_state.neurotransmitters
        
        # 血清素与多巴胺的平衡影响情绪稳定性
        nt.serotonin = 0.5 + (nt.dopamine - nt.cortisol) * 0.2
        
        # 去甲肾上腺素与唤醒度相关
        nt.norepinephrine = 0.3 + self.current_state.arousal * 0.3
        
        # GABA 与平静状态
        nt.gaba = 0.5 - self.current_state.arousal * 0.2 + self.current_state.dominance * 0.1
        
        nt.clamp()
    
    def _decay_neurotransmitters(self, time_delta: float):
        """神经递质衰减 (回归基线)"""
        nt = self.current_state.neurotransmitters
        
        # 基线值
        baselines = {
            "dopamine": 0.5,
            "cortisol": 0.3,
            "serotonin": 0.5,
            "norepinephrine": 0.4,
            "gaba": 0.5,
        }
        
        decay_rate = math.exp(-math.log(2) * time_delta / 1800)  # 30分钟半衰期
        
        for key, baseline in baselines.items():
            current = getattr(nt, key)
            setattr(nt, key, baseline + (current - baseline) * decay_rate)
        
        nt.clamp()
    
    # -------------------------------------------------------------------------
    # 状态历史
    # -------------------------------------------------------------------------
    
    def _record_state(self, old_state: EmotionState):
        """记录状态变更"""
        self.state_change_count += 1
        
        # 保存到历史
        self.history.append(self.current_state.copy())
        
        # 限制历史长度
        if len(self.history) > self.max_history_length:
            self.history = self.history[-self.max_history_length:]
    
    def get_state_history(
        self,
        limit: int = 100,
        since: Optional[datetime] = None,
    ) -> List[EmotionState]:
        """获取状态历史
        
        Args:
            limit: 返回数量限制
            since: 从何时开始
        
        Returns:
            状态历史列表
        """
        if since:
            return [
                s for s in self.history 
                if s.timestamp >= since
            ][-limit:]
        return self.history[-limit:]
    
    def get_recent_states(self, count: int = 10) -> List[EmotionState]:
        """获取最近的 n 个状态"""
        return self.history[-count:]
    
    # -------------------------------------------------------------------------
    # 状态转移
    # -------------------------------------------------------------------------
    
    def transition_to(
        self,
        target_state: EmotionState,
        transition_type: Literal["instant", "gradual", "blend"] = "instant",
        duration: float = 1.0,
    ) -> EmotionState:
        """
        状态转移
        
        Args:
            target_state: 目标状态
            transition_type: 转移类型
            duration: 过渡持续时间 (秒)
        
        Returns:
            转移后的状态
        """
        old_state = self.current_state.copy()
        
        if transition_type == "instant":
            self.current_state = target_state.copy()
            
        elif transition_type == "gradual":
            # 渐进转移 (在下次 update 时生效)
            self._pending_transition = target_state.copy()
            self._transition_duration = duration
            
        elif transition_type == "blend":
            # 混合两个状态
            blend_factor = 0.5
            self.current_state.pleasure = (
                old_state.pleasure * (1 - blend_factor) + 
                target_state.pleasure * blend_factor
            )
            self.current_state.arousal = (
                old_state.arousal * (1 - blend_factor) + 
                target_state.arousal * blend_factor
            )
            self.current_state.dominance = (
                old_state.dominance * (1 - blend_factor) + 
                target_state.dominance * blend_factor
            )
        
        self._update_timestamp()
        self._record_state(old_state)
        
        return self.current_state
    
    # -------------------------------------------------------------------------
    # 事件系统
    # -------------------------------------------------------------------------
    
    def _trigger_state_change(
        self, 
        old_state: EmotionState, 
        new_state: EmotionState
    ):
        """触发状态变更事件"""
        for callback in self.on_state_change:
            callback(old_state, new_state)
    
    def register_state_change_callback(
        self, 
        callback: Callable[[EmotionState, EmotionState], None]
    ):
        """注册状态变更回调"""
        self.on_state_change.append(callback)
    
    def register_regulation_callback(
        self, 
        callback: Callable[[EmotionState, RegulationResult], None]
    ):
        """注册调节回调"""
        self.on_regulation.append(callback)
    
    def register_decay_callback(
        self, 
        callback: Callable[[EmotionState, float], None]
    ):
        """注册衰减回调"""
        self.on_decay.append(callback)
    
    # -------------------------------------------------------------------------
    # 工具方法
    # -------------------------------------------------------------------------
    
    def _update_timestamp(self):
        """更新时间戳"""
        self.current_state.timestamp = datetime.now(timezone.utc)
        self.last_update_time = self.current_state.timestamp
    
    def get_current_state(self) -> EmotionState:
        """获取当前状态"""
        return self.current_state
    
    def get_pad(self) -> Dict[str, float]:
        """获取当前 PAD"""
        return self.current_state.to_pad_dict()
    
    def get_neurotransmitters(self) -> Dict[str, float]:
        """获取当前神经递质"""
        return self.current_state.neurotransmitters.to_dict()
    
    def reset(self):
        """重置状态"""
        self.current_state = EmotionState()
        self.occ_engine.reset()
        self.history.clear()
        self.last_update_time = datetime.now(timezone.utc)
        self.state_change_count = 0
        self.decay_count = 0
        self.regulation_count = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "state_change_count": self.state_change_count,
            "decay_count": self.decay_count,
            "regulation_count": self.regulation_count,
            "history_length": len(self.history),
            "current_intensity": self.current_state.get_intensity(),
            "current_emotion": self.current_state.get_emotion_label(),
            "regulation_success_rate": (
                self.current_state.regulation.get_success_rate()
            ),
        }
    
    def export_state(self) -> Dict[str, Any]:
        """导出完整状态"""
        return {
            "current_state": self.current_state.to_dict(),
            "occ_state": (
                self.current_state.occ_state.to_dict() 
                if self.current_state.occ_state else None
            ),
            "statistics": self.get_statistics(),
            "history": [s.to_dict() for s in self.history[-50:]],
        }
    
    def import_state(self, data: Dict[str, Any]):
        """导入状态"""
        if "current_state" in data:
            self.current_state = EmotionState.from_dict(data["current_state"])
        
        self.last_update_time = datetime.now(timezone.utc)


# ============================================================================
# 工厂函数
# ============================================================================

def create_state_manager(
    decay_enabled: bool = True,
    default_half_life: float = 3600,
    auto_regulate: bool = True,
) -> EmotionStateManager:
    """
    创建情绪状态管理器
    
    Args:
        decay_enabled: 是否启用衰减
        default_half_life: 默认半衰期
        auto_regulate: 是否自动调节
    
    Returns:
        EmotionStateManager 实例
    """
    return EmotionStateManager(
        decay_enabled=decay_enabled,
        default_half_life=default_half_life,
        auto_regulate=auto_regulate,
    )


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    "EmotionState",
    "EmotionStateManager",
    "Neurotransmitter",
    "NeurotransmitterState",
    "RegulationState",
    "create_state_manager",
]
