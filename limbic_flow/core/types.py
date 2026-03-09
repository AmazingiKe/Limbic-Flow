from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import time

if TYPE_CHECKING:
    from limbic_flow.core.articulation.action_event import ActionEvent

@dataclass
class CognitiveState:
    """
    [职责] 认知状态总线 - 贯穿整个 Pipeline 的核心数据对象
    [场景] 在各个器官之间传递，承载感知、情绪、记忆、表达和动作信息
    [可替换性] 核心数据结构，不可替换
    
    [OCC 支持]
    新增 OCC 相关字段，用于认知情绪模型:
    - occ_appraisal: 认知评估结果
    - occ_state: OCC 情绪状态
    - dominant_emotion: 主导情绪类型
    - emotion_intensity: 情绪强度
    """
    
    # Input Channel (输入通道)
    user_input: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    # Physiological Channel (生理通道)
    pad_vector: Dict[str, float] = field(default_factory=lambda: {"pleasure": 0.0, "arousal": 0.0, "dominance": 0.0})
    neurotransmitters: Dict[str, float] = field(default_factory=lambda: {"dopamine": 0.5, "cortisol": 0.3})
    environmental_pressure: float = 0.0 # 环境压力
    
    # OCC Channel (OCC 认知情绪) - 新增
    occ_appraisal: Optional[Any] = None  # 认知评估结果
    occ_state: Optional[Any] = None      # OCC 情绪状态
    dominant_emotion: str = ""           # 主导情绪类型
    emotion_intensity: float = 0.0      # 情绪强度
    
    # Memory Channel (记忆通道)
    query_vector: Optional[Any] = None  # numpy array
    memories: List[Dict[str, Any]] = field(default_factory=list)  # 主字段；raw_memories 为别名
    distorted_memories: List[Dict[str, Any]] = field(default_factory=list)

    # Expression Channel (表达通道)
    introspection: str = ""
    final_response_text: str = ""  # 主字段；final_text / content 为别名

    # Action Channel (动作通道)
    action_queue: List["ActionEvent"] = field(default_factory=list)

    @property
    def raw_memories(self) -> List[Dict[str, Any]]:
        """与 memories 同源，供病理中间件等读取。"""
        return self.memories

    @raw_memories.setter
    def raw_memories(self, value: List[Dict[str, Any]]) -> None:
        self.memories = value

    @property
    def final_text(self) -> str:
        return self.final_response_text

    @final_text.setter
    def final_text(self, value: str) -> None:
        self.final_response_text = value

    @property
    def content(self) -> str:
        return self.final_response_text

    @content.setter
    def content(self, value: str) -> None:
        self.final_response_text = value
