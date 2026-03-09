"""
社会情绪系统 - 基于研究文档实现

参考:
- MULTIAGENT_EMOTIONS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import math
import random


class AgentType(Enum):
    """智能体类型"""
    HUMAN = "human"
    AI = "ai"
    HYBRID = "hybrid"


@dataclass
class EmotionalAgent:
    """情绪智能体"""
    id: str
    agent_type: AgentType
    current_emotion: Dict[str, float] = field(default_factory=dict)
    personality: Dict[str, float] = field(default_factory=dict)
    relationships: Dict[str, float] = field(default_factory=dict)  # agent_id -> trust


class EmotionalContagion:
    """
    情绪传染
    
    研究:
    - 面部模仿
    - 声音韵律
    - 行为同步
    """
    
    def __init__(self):
        self.contagion_rate = 0.3
        self.individual_variation = 0.1
    
    def compute_contagion(
        self,
        source_emotion: Dict[str, float],
        target_susceptibility: float
    ) -> Dict[str, float]:
        """
        计算情绪传染
        
        传染强度 = 源情绪强度 × 目标易感性 × 传染率
        """
        infected = {}
        
        for emotion, intensity in source_emotion.items():
            # 基础传染
            base_contagion = intensity * self.contagion_rate
            
            # 个体差异
            variation = random.uniform(-self.individual_variation, self.individual_variation)
            
            # 易感性调节
            susceptibility = target_susceptibility * (1 + variation)
            
            infected[emotion] = base_contagion * susceptibility
        
        return infected


class GroupEmotionalDynamics:
    """
    群体情绪动力学
    
    研究:
    - 群体情绪气候
    - 情感协调
    - 集体情绪
    """
    
    def __init__(self):
        self.agents: Dict[str, EmotionalAgent] = {}
        self.group_mood = {"valence": 0.0, "arousal": 0.0}
        self.emotional_climate = "neutral"  # positive/negative/ambivalent
    
    def add_agent(self, agent: EmotionalAgent):
        """添加智能体"""
        self.agents[agent.id] = agent
    
    def compute_group_mood(self) -> Dict[str, float]:
        """计算群体情绪"""
        if not self.agents:
            return {"valence": 0.0, "arousal": 0.0}
        
        total_valence = 0.0
        total_arousal = 0.0
        
        for agent in self.agents.values():
            total_valence += agent.current_emotion.get("valence", 0.0)
            total_arousal += agent.current_emotion.get("arousal", 0.0)
        
        n = len(self.agents)
        
        self.group_mood = {
            "valence": total_valence / n,
            "arousal": total_arousal / n
        }
        
        return self.group_mood
    
    def determine_climate(self) -> str:
        """确定情绪气候"""
        mood = self.compute_group_mood()
        
        if mood["valence"] > 0.3:
            return "positive"
        elif mood["valence"] < -0.3:
            return "negative"
        else:
            return "ambivalent"


class SocialHierarchy:
    """
    社会层级
    
    研究:
    - 权力动态
    - 等级制度
    - 影响力
    """
    
    def __init__(self):
        self.positions: Dict[str, float] = {}  # agent_id -> position
        self.influence: Dict[str, float] = {}  # agent_id -> influence
    
    def set_position(self, agent_id: str, position: float):
        """设置位置 (-1=底层, 1=高层)"""
        self.positions[agent_id] = position
    
    def compute_influence(self, agent_id: str) -> float:
        """计算影响力"""
        position = self.positions.get(agent_id, 0.0)
        
        # 位置越高,影响力越大
        influence = (position + 1) / 2  # 转换到 [0, 1]
        
        self.influence[agent_id] = influence
        return influence


class EmpathySystem:
    """
    共情系统
    
    研究:
    - 认知共情
    - 情感共情
    - 共情响应
    """
    
    def __init__(self):
        self.cognitive_weight = 0.5
        self.emotional_weight = 0.5
    
    def compute_empathy(
        self,
        other_emotion: Dict[str, float],
        perspective_taking: float
    ) -> Dict[str, float]:
        """
        计算共情
        
        共情 = 认知共情 + 情感共情
        """
        # 认知共情: 理解他人情绪
        cognitive = perspective_taking * other_emotion
        
        # 情感共情: 感受他人情绪
        emotional = self.emotional_weight * other_emotion
        
        # 综合
        empathy = {}
        for key in other_emotion:
            empathy[key] = (
                cognitive.get(key, 0) * self.cognitive_weight +
                emotional.get(key, 0) * self.emotional_weight
            )
        
        return empathy
    
    def generate_response(
        self,
        empathy: Dict[str, float],
        response_type: str
    ) -> str:
        """生成共情响应"""
        if response_type == "validation":
            return "我理解你的感受"
        elif response_type == "mirroring":
            return "听起来你真的很..."
        elif response_type == "support":
            return "我在这里支持你"
        else:
            return "我听到了"


class EthicalEmotions:
    """
    道德情绪
    
    研究:
    - 羞耻/内疚
    - 道德情绪
    - 共情关注
    """
    
    def __init__(self):
        self.moral_threshold = 0.5
    
    def detect_guilt(
        self,
        action: str,
        moral_violation: float
    ) -> float:
        """检测内疚"""
        if moral_violation > self.moral_threshold:
            return moral_violation
        return 0.0
    
    def detect_shame(
        self,
        self_perception: str,
        social_standards: List[str]
    ) -> float:
        """检测羞耻"""
        # 简化: 检查是否符合社会标准
        violation = 0.0
        
        for standard in social_standards:
            if standard not in self_perception:
                violation += 0.2
        
        return min(1.0, violation)


class MultiAgentEmotionSystem:
    """
    多智能体情绪系统
    """
    
    def __init__(self):
        self.contagion = EmotionalContagion()
        self.group = GroupEmotionalDynamics()
        self.hierarchy = SocialHierarchy()
        self.empathy = EmpathySystem()
        self.ethical = EthicalEmotions()
    
    def simulate_interaction(
        self,
        agents: List[EmotionalAgent]
    ) -> Dict:
        """模拟交互"""
        # 添加智能体
        for agent in agents:
            self.group.add_agent(agent)
        
        # 情绪传染
        for agent in agents:
            for other in agents:
                if agent.id != other.id:
                    susceptibility = agent.personality.get("susceptibility", 0.5)
                    infection = self.contagion.compute_contagion(
                        other.current_emotion,
                        susceptibility
                    )
        
        # 群体情绪
        group_mood = self.group.compute_group_mood()
        climate = self.group.determine_climate()
        
        return {
            "group_mood": group_mood,
            "emotional_climate": climate
        }


if __name__ == "__main__":
    system = MultiAgentEmotionSystem()
    
    agents = [
        EmotionalAgent("1", AgentType.HUMAN, {"valence": 0.8, "arousal": 0.6}),
        EmotionalAgent("2", AgentType.AI, {"valence": 0.5, "arousal": 0.4}),
    ]
    
    result = system.simulate_interaction(agents)
    print(result)
