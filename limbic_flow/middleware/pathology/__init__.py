"""
病理中间件 - 记忆扭曲模块

[职责] 在记忆检索后、LLM思考前，根据当前情绪状态扭曲记忆
[设计] 可插拔的病理模块，支持多种病理类型

主要病理类型:
- 抑郁 (Depression): 屏蔽快乐记忆，压低愉悦度
- 阿尔茨海默 (Alzheimer): 高斯噪声 + 阻断近期记忆  
- 创伤后应激 (PTSD): 触发词强制检索创伤记忆
- 高敏感 (HSP): 低阈值放大情绪反应
"""

from abc import ABC, abstractmethod
import numpy as np
import time
import random
from typing import List, Dict, Any, Optional
from limbic_flow.core.types import CognitiveState


class PathologyMiddleware(ABC):
    """
    病理中间件接口 - 定义记忆扭曲的抽象方法
    """
    
    @abstractmethod
    def process(self, state: CognitiveState) -> CognitiveState:
        """处理认知状态，应用病理扭曲"""
        pass
    
    @abstractmethod
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """扭曲查询向量"""
        pass
    
    @abstractmethod
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """扭曲检索到的记忆"""
        pass


class BasePathologyMiddleware(PathologyMiddleware):
    """
    基础病理中间件 - 组合多个病理模块
    """
    
    def __init__(self, pathologies: List[Any] = None):
        self.pathologies = pathologies or []
    
    def add_pathology(self, pathology: Any) -> None:
        """添加病理模块"""
        self.pathologies.append(pathology)
    
    def process(self, state: CognitiveState) -> CognitiveState:
        """处理认知状态"""
        emotional_state = {
            "pleasure": state.pad_vector.get('pleasure', 0.0),
            "arousal": state.pad_vector.get('arousal', 0.0),
            "dominance": state.pad_vector.get('dominance', 0.0),
            "dopamine": state.neurotransmitters.get('dopamine', 0.5),
            "cortisol": state.neurotransmitters.get('cortisol', 0.3),
            "timestamp": state.timestamp
        }
        
        # 扭曲记忆
        state.distorted_memories = self.distort_memories(state.raw_memories, emotional_state)
        
        return state
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """依次应用各病理的查询扭曲"""
        distorted_vector = query_vector.copy()
        for pathology in self.pathologies:
            if pathology.should_apply(emotional_state):
                distorted_vector = pathology.distort_query(distorted_vector, emotional_state)
        return distorted_vector
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """依次应用各病理的记忆扭曲"""
        distorted_memories = list(memories)  # 深拷贝列表
        
        for pathology in self.pathologies:
            if pathology.should_apply(emotional_state):
                distorted_memories = pathology.distort_memories(distorted_memories, emotional_state)
        
        return distorted_memories


class Pathology(ABC):
    """病理基类"""
    
    @abstractmethod
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        """判断是否应该应用此病理"""
        pass
    
    @abstractmethod
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        """扭曲查询向量"""
        pass
    
    @abstractmethod
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """扭曲记忆列表"""
        pass


class DepressionPathology(Pathology):
    """
    抑郁模式 - 屏蔽快乐记忆，压低愉悦度感知
    
    [比喻] 就像抑郁症患者看世界是灰色的，好消息也感觉不到开心
    """
    
    def __init__(self, base_severity: float = 0.3):
        self.base_severity = base_severity
    
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        cortisol = emotional_state.get("cortisol", 0.0)
        pleasure = emotional_state.get("pleasure", 0.0)
        return cortisol > 0.4 or pleasure < -0.2
    
    def _calculate_severity(self, emotional_state: Dict[str, Any]) -> float:
        cortisol = emotional_state.get("cortisol", 0.3)
        cortisol_boost = max(0.0, (cortisol - 0.4) * 1.0)
        return min(1.0, self.base_severity + cortisol_boost)
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        severity = self._calculate_severity(emotional_state)
        distortion = np.full_like(query_vector, -0.1 * severity)
        return query_vector + distortion
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        severity = self._calculate_severity(emotional_state)
        distorted = []
        
        for memory in memories:
            mem_copy = {k: v.copy() if isinstance(v, dict) else v for k, v in memory.items()}
            memory_pleasure = mem_copy.get("pad", {}).get("pleasure", 0.0)
            
            # 屏蔽快乐记忆
            if memory_pleasure > 0.2:
                if random.random() < 0.8 * severity:
                    continue
            
            # 压低愉悦度
            if "pad" in mem_copy:
                mem_copy["pad"]["pleasure"] *= (1.0 - 0.8 * severity)
            
            distorted.append(mem_copy)
        
        return distorted


class AlzheimerPathology(Pathology):
    """
    阿尔茨海默模式 - 高斯噪声 + 阻断近期记忆
    
    [比喻] 就像老年痴呆患者，记得很久以前的事，但刚说的话转头就忘
    """
    
    def __init__(self, severity: float = 0.5):
        self.severity = severity
    
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        return True
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        noise = np.random.normal(0, 0.2 * self.severity, size=query_vector.shape)
        return query_vector + noise
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        distorted = []
        current_time = emotional_state.get("timestamp", time.time())
        
        for memory in memories:
            memory_time = memory.get("timestamp", 0)
            time_diff = current_time - memory_time
            
            # 近期记忆更容易被阻断
            if time_diff < 86400:  # 1天内
                if random.random() < 0.8 * self.severity:
                    continue
            elif time_diff < 604800:  # 1周内
                if random.random() < 0.5 * self.severity:
                    continue
            
            distorted.append(memory)
        
        return distorted


class PTSDPathology(Pathology):
    """
    创伤后应激障碍模式 - 触发词强制检索创伤记忆
    
    [比喻] 就像PTSD患者，听到某个关键词就会突然想起痛苦的回忆
    """
    
    # 常见触发词（可以配置）
    DEFAULT_TRIGGERS = [
        "去世", "死亡", "车祸", "事故", "伤害",
        "fire", "crash", "death", "accident",
    ]
    
    def __init__(self, severity: float = 0.5, triggers: List[str] = None):
        self.severity = severity
        self.triggers = triggers or self.DEFAULT_TRIGGERS
        self.trauma_memories: List[Dict[str, Any]] = []
    
    def add_trauma_memory(self, memory: Dict[str, Any]) -> None:
        """添加创伤记忆"""
        self.trauma_memories.append(memory)
    
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        # 需要结合上下文判断，暂时默认开启
        return len(self.trauma_memories) > 0
    
    def _check_triggers(self, text: str) -> bool:
        """检查是否包含触发词"""
        text_lower = text.lower()
        return any(trigger.lower() in text_lower for trigger in self.triggers)
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        return query_vector  # PTSD主要影响记忆检索
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        # 检查当前输入是否包含触发词
        user_input = emotional_state.get("user_input", "")
        
        if self._check_triggers(user_input):
            # 强制插入创伤记忆
            num_trauma = int(len(self.trauma_memories) * self.severity)
            trauma_sample = random.sample(
                self.trauma_memories, 
                min(num_trauma, len(self.trauma_memories))
            )
            return trauma_sample + list(memories)
        
        return list(memories)


class HSPPathology(Pathology):
    """
    高敏感人格模式 - 放大情绪反应
    
    [比喻] 就像高敏感的人，别人的一句话、一个眼神都会想很多
    """
    
    def __init__(self, sensitivity: float = 0.5):
        self.sensitivity = sensitivity
    
    def should_apply(self, emotional_state: Dict[str, Any]) -> bool:
        # 高敏感的人情绪阈值低，容易被触发
        arousal = emotional_state.get("arousal", 0.0)
        return abs(arousal) > 0.1  # 很低阈值就能触发
    
    def distort_query(self, query_vector: np.ndarray, emotional_state: Dict[str, Any]) -> np.ndarray:
        # 放大查询向量
        arousal = emotional_state.get("arousal", 0.0)
        amplification = 1.0 + abs(arousal) * self.sensitivity
        return query_vector * amplification
    
    def distort_memories(self, memories: List[Dict[str, Any]], emotional_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        # 放大记忆中的情绪
        distorted = []
        arousal = emotional_state.get("arousal", 0.0)
        
        for memory in memories:
            mem_copy = {k: v.copy() if isinstance(v, dict) else v for k, v in memory.items()}
            
            if "pad" in mem_copy:
                # 放大情绪强度
                for key in ["pleasure", "arousal", "dominance"]:
                    if key in mem_copy["pad"]:
                        sign = 1 if mem_copy["pad"][key] >= 0 else -1
                        mem_copy["pad"][key] = sign * min(
                            1.0, 
                            abs(mem_copy["pad"][key]) * (1.0 + self.sensitivity)
                        )
            
            distorted.append(mem_copy)
        
        return distorted


# 便捷函数
def create_pathology_middleware(
    enable_depression: bool = True,
    enable_alzheimer: bool = False,
    enable_ptsd: bool = False,
    enable_hsp: bool = False,
    **kwargs
) -> BasePathologyMiddleware:
    """
    创建病理中间件
    
    Args:
        enable_depression: 启用抑郁模式
        enable_alzheimer: 启用阿尔茨海默模式
        enable_ptsd: 启用PTSD模式
        enable_hsp: 启用高敏感模式
        **kwargs: 各病理的配置参数
    
    Returns:
        配置好的中间件
    """
    pathologies = []
    
    if enable_depression:
        pathologies.append(DepressionPathology(
            base_severity=kwargs.get("depression_severity", 0.3)
        ))
    
    if enable_alzheimer:
        pathologies.append(AlzheimerPathology(
            severity=kwargs.get("alzheimer_severity", 0.5)
        ))
    
    if enable_ptsd:
        pathologies.append(PTSDPathology(
            severity=kwargs.get("ptsd_severity", 0.5),
            triggers=kwargs.get("ptsd_triggers")
        ))
    
    if enable_hsp:
        pathologies.append(HSPPathology(
            sensitivity=kwargs.get("hsp_sensitivity", 0.5)
        ))
    
    return BasePathologyMiddleware(pathologies)
