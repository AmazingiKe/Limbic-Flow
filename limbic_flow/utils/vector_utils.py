"""
向量工具 - 向量相关工具函数
"""

import numpy as np
from typing import List, Optional


class VectorUtils:
    """向量操作工具"""
    
    @staticmethod
    def normalize(vector: np.ndarray) -> np.ndarray:
        """
        L2 归一化
        
        Args:
            vector: 输入向量
        
        Returns:
            归一化后的向量
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """
        余弦相似度
        
        Args:
            a: 向量 A
            b: 向量 B
        
        Returns:
            相似度 [-1, 1]
        """
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)
    
    @staticmethod
    def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
        """
        欧几里得距离
        
        Args:
            a: 向量 A
            b: 向量 B
        
        Returns:
            距离
        """
        return np.linalg.norm(a - b)
    
    @staticmethod
    def add_noise(vector: np.ndarray, std: float = 0.1) -> np.ndarray:
        """
        添加高斯噪声
        
        Args:
            vector: 输入向量
            std: 噪声标准差
        
        Returns:
            添加噪声后的向量
        """
        noise = np.random.normal(0, std, vector.shape)
        return vector + noise
    
    @staticmethod
    def interpolate(a: np.ndarray, b: np.ndarray, t: float = 0.5) -> np.ndarray:
        """
        线性插值
        
        Args:
            a: 向量 A
            b: 向量 B
            t: 插值因子 [0, 1]
        
        Returns:
            插值结果
        """
        return (1 - t) * a + t * b
    
    @staticmethod
    def pad_to_vector(
        pleasure: float, 
        arousal: float, 
        dominance: float,
        dim: int = 384
    ) -> np.ndarray:
        """
        将 PAD 值转换为向量
        
        用于将情绪状态转换为嵌入向量格式
        
        Args:
            pleasure: 愉悦度 [-1, 1]
            arousal: 唤醒度 [-1, 1]
            dominance: 控制度 [-1, 1]
            dim: 输出向量维度
        
        Returns:
            归一化的向量
        """
        # 基础向量
        base = np.array([pleasure, arousal, dominance])
        
        # 扩展到目标维度（简单复制）
        if dim > 3:
            vector = np.tile(base, (dim // 3) + 1)[:dim].astype(float)
        else:
            vector = base[:dim].astype(float)
        
        return VectorUtils.normalize(vector)


class TextUtils:
    """文本工具"""
    
    @staticmethod
    def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
        """
        截断文本
        
        Args:
            text: 输入文本
            max_length: 最大长度
            suffix: 后缀
        
        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        清理文本
        
        Args:
            text: 输入文本
        
        Returns:
            清理后的文本
        """
        # 移除多余空白
        text = " ".join(text.split())
        # 移除特殊字符（保留中文、英文、数字）
        import re
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        return text.strip()
    
    @staticmethod
    def split_sentences(text: str) -> List[str]:
        """
        分割句子
        
        Args:
            text: 输入文本
        
        Returns:
            句子列表
        """
        import re
        # 简单按标点分割
        sentences = re.split(r'[。！？.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
