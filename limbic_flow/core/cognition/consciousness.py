"""
意识与元认知系统 - 基于研究文档实现

参考:
- METACOGNITION_CONSCIOUSNESS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum
import math


class ConsciousnessLevel(Enum):
    """意识层级"""
    UNCONSCIOUS = "unconscious"
    PRECONSCIOUS = "preconscious"
    CONSCIOUS = "conscious"
    META_CONSCIOUS = "meta_conscious"


class IntegratedInformationMetrics:
    """
    整合信息理论 (IIT)
    
    研究: Φ (Phi) 计算
    """
    
    def __init__(self):
        self.phi_threshold = 0.5
    
    def calculate_phi(self, system_state: Dict) -> float:
        """计算整合信息 Φ"""
        # 简化: 基于状态数量和整合度
        n_elements = len(system_state)
        
        # 整合度 = 元素之间的相关性
        integration = sum(system_state.values()) / n_elements if n_elements > 0 else 0
        
        # Φ = 信息整合
        phi = integration * math.log2(n_elements) if n_elements > 1 else 0
        
        return min(1.0, phi)
    
    def is_conscious(self, phi: float) -> bool:
        """判断是否有意识"""
        return phi > self.phi_threshold


class GlobalWorkspaceTheory:
    """
    全局工作空间理论 (GWT)
    
    研究: 意识是信息在全局工作空间的广播
    """
    
    def __init__(self):
        self.workspace_content: List[str] = []
        self.modules = ["perception", "memory", "emotion", "action"]
    
    def broadcast(self, information: str):
        """广播信息到全局工作空间"""
        self.workspace_content.append(information)
    
    def access(self, module: str) -> List[str]:
        """模块访问工作空间"""
        return self.workspace_content


class ConsciousnessMonitor:
    """
    意识监控器
    """
    
    def __init__(self):
        self.iit = IntegratedInformationMetrics()
        self.gwt = GlobalWorkspaceTheory()
        self.current_level = ConsciousnessLevel.CONSCIOUS
    
    def assess_consciousness(self, system_state: Dict) -> Dict:
        """评估意识水平"""
        phi = self.iit.calculate_phi(system_state)
        
        level = ConsciousnessLevel.CONSCIOUS
        if phi < 0.2:
            level = ConsciousnessLevel.UNCONSCIOUS
        elif phi < 0.5:
            level = ConsciousnessLevel.PRECONSCIOUS
        elif phi < 0.8:
            level = ConsciousnessLevel.CONSCIOUS
        else:
            level = ConsciousnessLevel.META_CONSCIOUS
        
        return {
            "phi": phi,
            "level": level.value,
            "is_conscious": self.iit.is_conscious(phi)
        }


if __name__ == "__main__":
    monitor = ConsciousnessMonitor()
    state = {"perception": 0.8, "memory": 0.6, "emotion": 0.5}
    result = monitor.assess_consciousness(state)
    print(result)
