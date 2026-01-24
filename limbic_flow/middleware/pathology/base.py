from abc import ABC, abstractmethod
from typing import List
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

    @abstractmethod
    def apply(self, state: CognitiveState) -> CognitiveState:
        """
        应用病理扭曲

        Args:
            state: 当前的认知状态

        Returns:
            CognitiveState: 处理后的认知状态（通常包含被修改的 distorted_memories 或 pad_vector）
        """
        pass

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
