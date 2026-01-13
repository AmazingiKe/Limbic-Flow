from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """
    嵌入服务 - 用于生成文本的语义嵌入向量
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        初始化嵌入服务
        
        Args:
            model_name: 用于生成嵌入的模型名称
        """
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        获取文本的嵌入向量
        
        Args:
            text: 要嵌入的文本
        
        Returns:
            np.ndarray: 文本的嵌入向量
        """
        if not text:
            return np.zeros(self.embedding_dim)
        
        embedding = self.model.encode(text)
        return embedding
    
    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        批量获取文本的嵌入向量
        
        Args:
            texts: 要嵌入的文本列表
        
        Returns:
            List[np.ndarray]: 文本的嵌入向量列表
        """
        embeddings = self.model.encode(texts)
        return [np.array(emb) for emb in embeddings]