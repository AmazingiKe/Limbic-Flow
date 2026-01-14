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
    """
    
    # Input Channel (输入通道)
    user_input: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    
    # Physiological Channel (生理通道)
    pleasure: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0
    dopamine: float = 0.5  # 神经递质：奖励预期
    cortisol: float = 0.3  # 神经递质：压力水平
    environmental_pressure: float = 0.0 # 环境压力
    
    # Memory Channel (记忆通道)
    query_vector: Optional[Any] = None # numpy array
    raw_memories: List[Dict[str, Any]] = field(default_factory=list)
    distorted_memories: List[Dict[str, Any]] = field(default_factory=list)
    
    # Expression Channel (表达通道)
    introspection: str = "" # 思维链/内省
    content: str = "" # 最终回复文本
    
    # Action Channel (动作通道)
    action_queue: List['ActionEvent'] = field(default_factory=list)
