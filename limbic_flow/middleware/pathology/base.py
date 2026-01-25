from abc import ABC, abstractmethod
from typing import Any, Dict, List
from limbic_flow.core.types import CognitiveState

class PathologyBase(ABC):
    """
    病理模式抽象基类
    所有的病理模式（如阿尔茨海默、抑郁症、PTSD）都必须继承此类
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """病理模式名称"""
        pass

    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        return True

    def distort_query(self, query_vector: Any, emotional_state: Dict[str, Any]) -> Any:
        return query_vector

    def distort_memories(
        self,
        memories: List[Dict[str, Any]],
        emotional_state: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        return memories

    def apply(self, state: CognitiveState) -> CognitiveState:
        emotional_state = self._build_emotional_state(state)
        if not self.should_apply(emotional_state):
            return state
        if not state.distorted_memories and state.memories:
            import copy
            state.distorted_memories = copy.deepcopy(state.memories)
        if state.distorted_memories:
            state.distorted_memories = self.distort_memories(
                state.distorted_memories,
                emotional_state,
            )
        return state

    def _build_emotional_state(self, state: CognitiveState) -> Dict[str, Any]:
        return {
            "pleasure": state.pad_vector["pleasure"],
            "arousal": state.pad_vector["arousal"],
            "dominance": state.pad_vector["dominance"],
            "dopamine": state.neurotransmitters["dopamine"],
            "cortisol": state.neurotransmitters["cortisol"],
            "timestamp": state.timestamp,
        }

class PathologyMiddlewareManager:
    """
    病理中间件管理器
    负责按顺序执行注册的病理模式
    """
    def __init__(self):
        self._pathologies: List[PathologyBase] = []

    def register(self, pathology: PathologyBase):
        """注册一个新的病理模式"""
        self._pathologies.append(pathology)
        print(f"🧩 已加载病理中间件: {pathology.name}")

    def _build_emotional_state(self, state: CognitiveState) -> Dict[str, Any]:
        return {
            "pleasure": state.pad_vector["pleasure"],
            "arousal": state.pad_vector["arousal"],
            "dominance": state.pad_vector["dominance"],
            "dopamine": state.neurotransmitters["dopamine"],
            "cortisol": state.neurotransmitters["cortisol"],
            "timestamp": state.timestamp,
        }

    def distort_query(self, state: CognitiveState) -> CognitiveState:
        if state.query_vector is None:
            return state
        emotional_state = self._build_emotional_state(state)
        for pathology in self._pathologies:
            try:
                if pathology.should_apply(emotional_state):
                    state.query_vector = pathology.distort_query(
                        state.query_vector,
                        emotional_state,
                    )
            except Exception as e:
                print(
                    f"[pathology] query distortion failed for {pathology.name}: {e}"
                )
                continue
        return state

    def process(self, state: CognitiveState) -> CognitiveState:
        """
        依次应用所有已注册的病理模式
        """
        # 默认情况下，如果还没被任何中间件处理，distorted_memories 初始就是 raw_memories
        if not state.distorted_memories and state.memories:
             # 深拷贝以防修改原始数据
            import copy
            state.distorted_memories = copy.deepcopy(state.memories)

        for pathology in self._pathologies:
            try:
                state = pathology.apply(state)
            except Exception as e:
                print(f"⚠️ 病理中间件 {pathology.name} 执行出错: {e}")
                # 出错时不中断流程，继续下一个中间件
                continue

        return state
