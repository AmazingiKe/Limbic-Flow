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
    pad_vector: Dict[str, float] = field(default_factory=lambda: {"pleasure": 0.0, "arousal": 0.0, "dominance": 0.0})
    neurotransmitters: Dict[str, float] = field(default_factory=lambda: {"dopamine": 0.5, "cortisol": 0.3})
    environmental_pressure: float = 0.0 # 环境压力
    
    # Memory Channel (记忆通道)
    query_vector: Optional[Any] = None # numpy array
    memories: List[Dict[str, Any]] = field(default_factory=list) # Renamed from raw_memories? User used 'memories'
    raw_memories: List[Dict[str, Any]] = field(default_factory=list) # Keep for compatibility or use user's name
    distorted_memories: List[Dict[str, Any]] = field(default_factory=list)
    
    # Expression Channel (表达通道)
    introspection: str = "" # 思维链/内省
    final_response_text: str = "" # 最终回复文本
    content: str = "" # Keep for compatibility, alias to final_response_text?
    
    # Action Channel (动作通道)
    action_queue: List['ActionEvent'] = field(default_factory=list)
