from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class NeocortexInterface(ABC):
    """
    新皮层接口 - 定义语义知识存储和检索的抽象方法
    """
    
    @abstractmethod
    def store_knowledge(self, key: str, value: Any) -> bool:
        """
        存储语义知识
        
        Args:
            key: 知识键
            value: 知识值
        
        Returns:
            bool: 存储是否成功
        """
        pass
    
    @abstractmethod
    def retrieve_knowledge(self, key: str) -> Optional[Any]:
        """
        检索语义知识
        
        Args:
            key: 知识键
        
        Returns:
            Optional[Any]: 知识值，如果不存在则返回None
        """
        pass
    
    @abstractmethod
    def store_relationship(self, subject: str, predicate: str, object: str) -> bool:
        """
        存储关系
        
        Args:
            subject: 主体
            predicate: 谓词
            object: 客体
        
        Returns:
            bool: 存储是否成功
        """
        pass
    
    @abstractmethod
    def retrieve_relationships(self, subject: str = None, predicate: str = None, object: str = None) -> List[Dict[str, str]]:
        """
        检索关系
        
        Args:
            subject: 主体 (可选)
            predicate: 谓词 (可选)
            object: 客体 (可选)
        
        Returns:
            List[Dict[str, str]]: 关系列表
        """
        pass

class MockNeocortex(NeocortexInterface):
    """
    模拟新皮层 - 用于开发和测试
    """
    
    def __init__(self):
        self.knowledge_store = {}
        self.relationships = []
    
    def store_knowledge(self, key: str, value: Any) -> bool:
        """
        存储语义知识
        
        Args:
            key: 知识键
            value: 知识值
        
        Returns:
            bool: 存储是否成功
        """
        self.knowledge_store[key] = value
        return True
    
    def retrieve_knowledge(self, key: str) -> Optional[Any]:
        """
        检索语义知识
        
        Args:
            key: 知识键
        
        Returns:
            Optional[Any]: 知识值，如果不存在则返回None
        """
        return self.knowledge_store.get(key)
    
    def store_relationship(self, subject: str, predicate: str, object: str) -> bool:
        """
        存储关系
        
        Args:
            subject: 主体
            predicate: 谓词
            object: 客体
        
        Returns:
            bool: 存储是否成功
        """
        self.relationships.append({
            "subject": subject,
            "predicate": predicate,
            "object": object
        })
        return True
    
    def retrieve_relationships(self, subject: str = None, predicate: str = None, object: str = None) -> List[Dict[str, str]]:
        """
        检索关系
        
        Args:
            subject: 主体 (可选)
            predicate: 谓词 (可选)
            object: 客体 (可选)
        
        Returns:
            List[Dict[str, str]]: 关系列表
        """
        result = []
        for relationship in self.relationships:
            if subject and relationship["subject"] != subject:
                continue
            if predicate and relationship["predicate"] != predicate:
                continue
            if object and relationship["object"] != object:
                continue
            result.append(relationship)
        return result