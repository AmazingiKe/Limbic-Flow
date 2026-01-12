from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict, Any, Tuple

class HippocampusInterface(ABC):
    """
    海马体接口 - 定义记忆存储和检索的抽象方法
    """
    
    @abstractmethod
    def store_memory(self, episodic_memory: Dict[str, Any]) -> str:
        """
        存储情景记忆
        
        Args:
            episodic_memory: 包含事件向量、主观感受和时间戳的记忆
        
        Returns:
            str: 记忆ID
        """
        pass
    
    @abstractmethod
    def retrieve_memories(self, query_vector: np.ndarray, limit: int = 5) -> List[Dict[str, Any]]:
        """
        检索记忆
        
        Args:
            query_vector: 查询向量
            limit: 返回的记忆数量限制
        
        Returns:
            List[Dict[str, Any]]: 检索到的记忆列表
        """
        pass

class MockHippocampus(HippocampusInterface):
    """
    模拟海马体 - 用于开发和测试
    """
    
    def __init__(self):
        self.memories = {}
        self.next_id = 0
    
    def store_memory(self, episodic_memory: Dict[str, Any]) -> str:
        """
        存储情景记忆
        
        Args:
            episodic_memory: 包含事件向量、主观感受和时间戳的记忆
        
        Returns:
            str: 记忆ID
        """
        memory_id = str(self.next_id)
        self.next_id += 1
        
        # 确保记忆包含必要字段
        if "vector" not in episodic_memory:
            raise ValueError("Memory must contain a vector")
        if "pad" not in episodic_memory:
            episodic_memory["pad"] = {"pleasure": 0.0, "arousal": 0.0, "dominance": 0.0}
        if "timestamp" not in episodic_memory:
            import time
            episodic_memory["timestamp"] = time.time()
        
        self.memories[memory_id] = episodic_memory
        return memory_id
    
    def retrieve_memories(self, query_vector: np.ndarray, limit: int = 5) -> List[Dict[str, Any]]:
        """
        检索记忆 - 使用余弦相似度
        
        Args:
            query_vector: 查询向量
            limit: 返回的记忆数量限制
        
        Returns:
            List[Dict[str, Any]]: 检索到的记忆列表
        """
        if not self.memories:
            return []
        
        # 计算与每个记忆的相似度
        similarities = []
        for memory_id, memory in self.memories.items():
            memory_vector = np.array(memory["vector"])
            # 计算余弦相似度
            similarity = np.dot(query_vector, memory_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(memory_vector)
            )
            similarities.append((similarity, memory))
        
        # 按相似度排序并返回前N个
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [memory for _, memory in similarities[:limit]]