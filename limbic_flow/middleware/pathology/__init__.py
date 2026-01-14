from abc import ABC, abstractmethod
import numpy as np
import time
from typing import List, Dict, Any, Optional
from limbic_flow.core.types import CognitiveState


class PathologyMiddleware(ABC):
    """
    [职责] 病理中间件接口 - 定义记忆扭曲的抽象方法
    [场景] 记忆检索后，LLM 思考前
    [可替换性] 可插拔的病理模块
    """
    
    def process(self, state: CognitiveState) -> CognitiveState:
        """
        [职责] 处理认知状态，应用病理扭曲
        [场景] Pipeline 调度调用
        """
        emotional_state = {
            "pleasure": state.pad_vector['pleasure'],
            "arousal": state.pad_vector['arousal'],
            "dominance": state.pad_vector['dominance'],
            "dopamine": state.neurotransmitters['dopamine'],
            "cortisol": state.neurotransmitters['cortisol'],
            "timestamp": state.timestamp
        }
        
        # 扭曲记忆
        # 假设海马体已经将原始记忆填入 raw_memories
        state.distorted_memories = self.distort_memories(state.raw_memories, emotional_state)
        
        return state

    @abstractmethod
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """
        扭曲查询向量
        """
        pass
    
    @abstractmethod
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        扭曲检索到的记忆
        """
        pass

class BasePathologyMiddleware(PathologyMiddleware):
    """
    基础病理中间件 - 实现默认行为
    """
    
    def __init__(self):
        """
        初始化基础病理中间件
        """
        self.pathologies = []
    
    def add_pathology(self, pathology):
        """
        添加病理模块
        """
        self.pathologies.append(pathology)
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        distorted_vector = query_vector.copy()
        for pathology in self.pathologies:
            if pathology.should_apply(emotional_state):
                distorted_vector = pathology.distort_query(distorted_vector, emotional_state)
        return distorted_vector
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        distorted_memories = memories # Create a copy inside the loop if needed, but for list of dicts, be careful.
        # Actually, let's copy the list structure first
        distorted_memories = list(memories) 
        
        for pathology in self.pathologies:
            if pathology.should_apply(emotional_state):
                distorted_memories = pathology.distort_memories(distorted_memories, emotional_state)
        
        return distorted_memories

class DepressionPathology:
    """
    [职责] 抑郁模式病理 - 降低P值，屏蔽快乐记忆
    [逻辑] 皮质醇越高 -> 权重越大 -> 快乐记忆越不可见
    """
    
    def __init__(self, base_severity: float = 0.3):
        self.base_severity = base_severity
    
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        # 只要皮质醇高或愉悦度低就应用
        cortisol = emotional_state.get("cortisol", 0.0)
        pleasure = emotional_state.get("pleasure", 0.0)
        return cortisol > 0.4 or pleasure < -0.2
    
    def _calculate_dynamic_severity(self, emotional_state: Dict[str, Any]) -> float:
        # 动态权重：皮质醇越高，严重程度越高
        cortisol = emotional_state.get("cortisol", 0.3)
        # 映射: cortisol 0.4 -> 0.0 boost, 1.0 -> 0.6 boost
        cortisol_boost = max(0.0, (cortisol - 0.4) * 1.0)
        
        return min(1.0, self.base_severity + cortisol_boost)

    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        severity = self._calculate_dynamic_severity(emotional_state)
        # 负向偏移
        distortion = np.full_like(query_vector, -0.1 * severity)
        return query_vector + distortion
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        severity = self._calculate_dynamic_severity(emotional_state)
        distorted_memories = []
        
        for memory in memories:
            # 深拷贝记忆对象以免修改原始数据 (Simple dict copy)
            mem_copy = memory.copy()
            if "pad" in memory:
                mem_copy["pad"] = memory["pad"].copy()
            
            memory_pleasure = mem_copy.get("pad", {}).get("pleasure", 0.0)
            
            # 屏蔽快乐记忆
            if memory_pleasure > 0.2:
                # 严重程度越高，屏蔽概率越大
                if np.random.random() < 0.8 * severity:
                    continue
            
            # 压低记忆的愉悦度 (P值)
            if "pad" in mem_copy:
                # 越严重的抑郁，对快乐的感知越弱
                mem_copy["pad"]["pleasure"] *= (1.0 - 0.8 * severity)
            
            distorted_memories.append(mem_copy)
        
        return distorted_memories

class AlzheimerPathology:
    """
    阿尔兹海默模式病理 - 注入高斯噪声，随机阻断近期记忆
    """
    
    def __init__(self, severity: float = 0.5):
        """
        初始化阿尔兹海默模式
        
        Args:
            severity: 严重程度 [0, 1]
        """
        self.severity = severity
    
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        """
        判断是否应该应用此病理
        
        Args:
            emotional_state: 当前情绪状态
        
        Returns:
            bool: 是否应用
        """
        # 可以根据特定标志或状态判断
        return True
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """
        扭曲查询向量 - 注入高斯噪声
        
        Args:
            query_vector: 原始查询向量
            emotional_state: 当前情绪状态
        
        Returns:
            np.ndarray: 扭曲后的查询向量
        """
        # 注入高斯噪声
        noise = np.random.normal(0, 0.2 * self.severity, size=query_vector.shape)
        return query_vector + noise
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        扭曲检索到的记忆 - 阻断近期记忆，保留远期记忆
        
        Args:
            memories: 原始记忆列表
            emotional_state: 当前情绪状态
        
        Returns:
            List[Dict[str, Any]]: 扭曲后的记忆列表
        """
        distorted_memories = []
        current_time = emotional_state.get("timestamp", time.time())
        
        for memory in memories:
            memory_time = memory.get("timestamp", 0)
            time_diff = current_time - memory_time
            
            # 近期记忆被阻断的概率更高
            if time_diff < 86400:  # 1天内
                if np.random.random() < 0.8 * self.severity:
                    continue
            elif time_diff < 604800:  # 1周内
                if np.random.random() < 0.5 * self.severity:
                    continue
            
            distorted_memories.append(memory)
        
        return distorted_memories