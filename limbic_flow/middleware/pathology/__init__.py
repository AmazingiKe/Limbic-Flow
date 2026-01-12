from abc import ABC, abstractmethod
import numpy as np
import time
from typing import List, Dict, Any, Optional
from limbic_flow.core.hippocampus import HippocampusInterface

class PathologyMiddleware(ABC):
    """
    病理中间件接口 - 定义记忆扭曲的抽象方法
    """
    
    @abstractmethod
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """
        扭曲查询向量
        
        Args:
            query_vector: 原始查询向量
            emotional_state: 当前情绪状态
        
        Returns:
            np.ndarray: 扭曲后的查询向量
        """
        pass
    
    @abstractmethod
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        扭曲检索到的记忆
        
        Args:
            memories: 原始记忆列表
            emotional_state: 当前情绪状态
        
        Returns:
            List[Dict[str, Any]]: 扭曲后的记忆列表
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
        
        Args:
            pathology: 病理模块实例
        """
        self.pathologies.append(pathology)
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """
        扭曲查询向量 - 应用所有病理模块
        
        Args:
            query_vector: 原始查询向量
            emotional_state: 当前情绪状态
        
        Returns:
            np.ndarray: 扭曲后的查询向量
        """
        distorted_vector = query_vector.copy()
        
        for pathology in self.pathologies:
            if pathology.should_apply(emotional_state):
                distorted_vector = pathology.distort_query(distorted_vector, emotional_state)
        
        return distorted_vector
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        扭曲检索到的记忆 - 应用所有病理模块
        
        Args:
            memories: 原始记忆列表
            emotional_state: 当前情绪状态
        
        Returns:
            List[Dict[str, Any]]: 扭曲后的记忆列表
        """
        distorted_memories = memories.copy()
        
        for pathology in self.pathologies:
            if pathology.should_apply(emotional_state):
                distorted_memories = pathology.distort_memories(distorted_memories, emotional_state)
        
        return distorted_memories

class DepressionPathology:
    """
    抑郁模式病理 - 降低P值，屏蔽快乐记忆
    """
    
    def __init__(self, severity: float = 0.5):
        """
        初始化抑郁模式
        
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
        # 当愉悦度低于阈值时应用
        return emotional_state.get("pleasure", 0.0) < -0.3
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """
        扭曲查询向量 - 降低积极情绪相关维度
        
        Args:
            query_vector: 原始查询向量
            emotional_state: 当前情绪状态
        
        Returns:
            np.ndarray: 扭曲后的查询向量
        """
        # 在实际实现中，这里应该根据情绪向量的维度进行有针对性的扭曲
        # 简化实现：添加负向偏移
        distortion = np.full_like(query_vector, -0.1 * self.severity)
        return query_vector + distortion
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        扭曲检索到的记忆 - 屏蔽快乐记忆，降低记忆的积极程度
        
        Args:
            memories: 原始记忆列表
            emotional_state: 当前情绪状态
        
        Returns:
            List[Dict[str, Any]]: 扭曲后的记忆列表
        """
        distorted_memories = []
        
        for memory in memories:
            # 降低快乐记忆的权重
            memory_pleasure = memory.get("pad", {}).get("pleasure", 0.0)
            
            if memory_pleasure > 0.3:
                # 快乐记忆被屏蔽的概率
                if np.random.random() < 0.7 * self.severity:
                    continue
            
            # 降低记忆的积极程度
            if "pad" in memory:
                memory["pad"]["pleasure"] *= (1 - 0.5 * self.severity)
            
            distorted_memories.append(memory)
        
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