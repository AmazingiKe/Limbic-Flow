from abc import ABC, abstractmethod
import numpy as np
import json
import os
from typing import List, Dict, Any, Tuple
from limbic_flow.utils.logger import get_logger

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

class FileHippocampus(HippocampusInterface):
    """
    文件海马体 - 基于文件的持久化存储实现
    """
    
    def __init__(self, storage_path: str = "./memory_store.json"):
        """
        初始化文件海马体
        
        Args:
            storage_path: 存储文件路径
        """
        self.logger = get_logger("FileHippocampus")
        self.storage_path = storage_path
        self.memories = {}
        self.next_id = 0
        self._load_from_file()
    
    def _load_from_file(self):
        """
        从文件加载记忆
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = data.get('memories', {})
                    self.next_id = data.get('next_id', 0)
                    self.logger.info(f"成功从文件加载 {len(self.memories)} 条记忆")
            except Exception as e:
                self.logger.error(f"加载记忆失败: {str(e)}", exc_info=True)
                self.memories = {}
                self.next_id = 0
    
    def _save_to_file(self):
        """
        保存记忆到文件
        """
        try:
            data = {
                'memories': self.memories,
                'next_id': self.next_id
            }
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug(f"成功保存 {len(self.memories)} 条记忆到文件")
        except Exception as e:
            self.logger.error(f"保存记忆失败: {str(e)}", exc_info=True)
    
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
        self._save_to_file()
        return memory_id
    
    def retrieve_memories(self, query_vector: np.ndarray, limit: int = 5) -> List[Dict[str, Any]]:
        """
        检索记忆 - 使用余弦相似度并考虑记忆重要性
        
        Args:
            query_vector: 查询向量
            limit: 返回的记忆数量限制
        
        Returns:
            List[Dict[str, Any]]: 检索到的记忆列表
        """
        if not self.memories:
            return []
        
        import time
        
        # 计算与每个记忆的相似度和重要性
        scored_memories = []
        current_time = time.time()
        
        for memory_id, memory in self.memories.items():
            memory_vector = np.array(memory["vector"])
            
            # 计算余弦相似度
            similarity = np.dot(query_vector, memory_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(memory_vector)
            )
            
            # 计算记忆重要性得分
            importance_score = 0.0
            
            # 1. 时间衰减因子 - 越近的记忆越重要
            time_diff = current_time - memory.get("timestamp", current_time)
            # 时间衰减，半衰期为24小时
            time_decay = np.exp(-np.log(2) * time_diff / (24 * 3600))
            importance_score += time_decay * 0.4
            
            # 2. 情绪强度 - 情绪波动大的记忆更重要
            pad = memory.get("pad", {})
            pleasure = abs(pad.get("pleasure", 0.0))
            arousal = abs(pad.get("arousal", 0.0))
            dominance = abs(pad.get("dominance", 0.0))
            emotional_intensity = (pleasure + arousal + dominance) / 3.0
            importance_score += emotional_intensity * 0.3
            
            # 3. 用户信息 - 包含用户信息的记忆更重要
            user_info = memory.get("user_info", {})
            if user_info and "name" in user_info:
                importance_score += 0.3
            
            # 综合得分
            total_score = similarity * 0.7 + importance_score * 0.3
            scored_memories.append((total_score, memory))
        
        # 按综合得分排序并返回前N个
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [memory for _, memory in scored_memories[:limit]]