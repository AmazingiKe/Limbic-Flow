"""
社会认知系统 - 基于研究文档
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SocialAgent:
    """社会智能体"""
    id: str
    relationship: float = 0.5  # -1 到 1
    trust: float = 0.5


class TheoryOfMind:
    """心智理论"""
    
    def __init__(self):
        self.mental_models: Dict[str, Dict] = {}
    
    def update_belief(
        self,
        agent_id: str,
        belief: str,
        confidence: float
    ):
        """更新信念"""
        if agent_id not in self.mental_models:
            self.mental_models[agent_id] = {}
        
        self.mental_models[agent_id][belief] = confidence
    
    def predict_behavior(
        self,
        agent_id: str,
        context: str
    ) -> str:
        """预测行为"""
        model = self.mental_models.get(agent_id, {})
        
        if "aggressive" in context:
            return "defensive"
        elif "friendly" in context:
            return "approaching"
        
        return "neutral"
    
    def infer_emotion(
        self,
        agent_id: str,
        observation: str
    ) -> Dict[str, float]:
        """推断情绪"""
        emotion = {"joy": 0.0, "sadness": 0.0, "anger": 0.0}
        
        if "smile" in observation:
            emotion["joy"] = 0.7
        elif "frown" in observation:
            emotion["sadness"] = 0.6
        
        return emotion


class EmpathyEngine:
    """共情引擎"""
    
    def __init__(self):
        self.theory_of_mind = TheoryOfMind()
    
    def compute_perspective_taking(
        self,
        agent_id: str,
        situation: str
    ) -> float:
        """换位思考"""
        return 0.6
    
    def generate_empathic_response(
        self,
        other_emotion: Dict[str, float]
    ) -> str:
        """生成共情响应"""
        if other_emotion.get("sadness", 0) > 0.5:
            return "我理解你的难过"
        elif other_emotion.get("joy", 0) > 0.5:
            return "真为你高兴!"
        
        return "我听到了"


class SocialReasoning:
    """社会推理"""
    
    def __init__(self):
        self.relationships: Dict[str, SocialAgent] = {}
    
    def update_relationship(
        self,
        agent_id: str,
        interaction_quality: float
    ):
        """更新关系"""
        if agent_id not in self.relationships:
            self.relationships[agent_id] = SocialAgent(agent_id)
        
        agent = self.relationships[agent_id]
        agent.relationship = max(-1, min(1, 
            agent.relationship + (interaction_quality - 0.5) * 0.2
        ))
    
    def get_social_decision(
        self,
        agent_id: str,
        action: str
    ) -> str:
        """获取社会决策"""
        agent = self.relationships.get(agent_id)
        
        if not agent:
            return "neutral"
        
        if agent.relationship > 0.5:
            return "cooperate"
        elif agent.relationship < -0.3:
            return "compete"
        
        return "neutral"


if __name__ == "__main__":
    tom = TheoryOfMind()
    tom.update_belief("person1", "hungry", 0.8)
    print(tom.predict_behavior("person1", "aggressive"))
