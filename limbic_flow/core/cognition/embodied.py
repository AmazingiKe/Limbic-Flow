"""
具身认知系统 - 基于研究文档实现

参考:
- EMBODIED_COGNITION.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math
import random


class SensoryModality(Enum):
    """感官模态"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    PROPRIOCEPTIVE = "proprioceptive"  # 本体感觉
    VESTIBULAR = "vestibular"          # 前庭感觉
    TACTILE = "tactile"                # 触觉
    OLFACTORY = "olfactory"            # 嗅觉
    GUSTATORY = "gustatory"            # 味觉


class MotorCapability(Enum):
    """运动能力"""
    REACH = "reach"
    GRASP = "grasp"
    WALK = "walk"
    RUN = "run"
    MANIPULATE = "manipulate"
    COMMUNICATE = "communicate"


@dataclass
class BodyState:
    """身体状态"""
    # 位置和方向
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    orientation: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # roll, pitch, yaw
    
    # 运动状态
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    is_moving: bool = False
    
    # 生理状态
    energy_level: float = 1.0  # 0-1
    fatigue: float = 0.0       # 0-1
    arousal_level: float = 0.5  # 0-1


@dataclass
class SensorimotorPattern:
    """感觉运动模式"""
    modality: SensoryModality
    content: str
    intensity: float
    timestamp: float


class EmbodiedCognitionSystem:
    """
    具身认知系统
    
    研究:
    - 身体参与认知过程
    - 感觉运动整合
    - 概念根植于身体经验
    """
    
    def __init__(self):
        self.body_state = BodyState()
        
        # 感觉运动历史
        self.sensor_history: List[SensorimotorPattern] = []
        
        # 概念映射
        self.grounded_concepts: Dict[str, List[str]] = {}
        
        # 初始化概念映射
        self._init_concept_mappings()
    
    def _init_concept_mappings(self):
        """初始化概念映射"""
        # 基于 Lakoff & Johnson 隐喻理论
        self.grounded_concepts = {
            # 方位隐喻
            "happy": ["up", "light", "open"],
            "sad": ["down", "heavy", "closed"],
            "power": ["up", "strong", "big"],
            "control": ["up", "above", "over"],
            "emotion": ["warm", "fluid", "physical"],
            
            # 身体动作
            "understand": ["grasp", "take_in"],
            "attention": ["focus", "direct"],
            "time": ["flow", "pass", "move"],
            "change": ["move", "turn", "shift"],
            
            # 感官经验
            "idea": ["bright", "clear"],
            "confusion": ["fuzzy", "dark"],
            "clarity": ["bright", "sharp"],
        }
    
    def update_body_state(
        self,
        position: Optional[Tuple[float, float, float]] = None,
        velocity: Optional[Tuple[float, float, float]] = None,
        energy: Optional[float] = None
    ):
        """更新身体状态"""
        if position:
            self.body_state.position = position
        
        if velocity:
            self.body_state.velocity = velocity
            self.body_state.is_moving = any(abs(v) > 0.01 for v in velocity)
        
        if energy is not None:
            self.body_state.energy_level = max(0, min(1, energy))
    
    def process_sensory_input(
        self,
        modality: SensoryModality,
        content: str,
        intensity: float
    ) -> SensorimotorPattern:
        """处理感官输入"""
        import time
        
        pattern = SensorimotorPattern(
            modality=modality,
            content=content,
            intensity=intensity,
            timestamp=time.time()
        )
        
        self.sensor_history.append(pattern)
        
        # 限制历史长度
        if len(self.sensor_history) > 1000:
            self.sensor_history = self.sensor_history[-500:]
        
        return pattern
    
    def get_grounded_meaning(self, concept: str) -> List[str]:
        """获取概念的具身含义"""
        return self.grounded_concepts.get(concept, [])
    
    def generate_embodied_response(
        self,
        emotion: str,
        intensity: float
    ) -> Dict:
        """
        生成具身响应
        
        情绪产生身体反应
        """
        # 情绪到身体的映射
        body_responses = {
            "joy": {
                "posture": "upright",
                "movement": "energetic",
                "tension": "relaxed",
                "energy_change": 0.2
            },
            "sadness": {
                "posture": "slumped",
                "movement": "slow",
                "tension": "relaxed",
                "energy_change": -0.2
            },
            "anger": {
                "posture": "tense",
                "movement": "forceful",
                "tension": "high",
                "energy_change": 0.1
            },
            "fear": {
                "posture": "tense",
                "movement": "alert",
                "tension": "high",
                "energy_change": 0.1
            },
            "surprise": {
                "posture": "alert",
                "movement": "sudden",
                "tension": "moderate",
                "energy_change": 0.15
            }
        }
        
        response = body_responses.get(emotion, {
            "posture": "neutral",
            "movement": "normal",
            "tension": "moderate",
            "energy_change": 0.0
        })
        
        # 根据强度调整
        if intensity > 0.7:
            response["movement"] = "intensified_" + response["movement"]
        
        return response
    
    def update_energy(self, delta: float):
        """更新能量"""
        self.body_state.energy_level = max(0, min(1, 
            self.body_state.energy_level + delta
        ))
        
        # 能量影响疲劳
        if self.body_state.energy_level < 0.3:
            self.body_state.fatigue = min(1.0, self.body_state.fatigue + 0.01)
        elif self.body_state.energy_level > 0.7:
            self.body_state.fatigue = max(0, self.body_state.fatigue - 0.01)


class SensorimotorIntegration:
    """
    感觉运动整合
    
    研究: 感觉运动协调和前向模型
    """
    
    def __init__(self):
        # 前向模型: 预测运动结果
        self.forward_models: Dict[str, Dict] = {}
        
        # 运动命令到感觉的映射
        self.effference_copies: Dict[str, List[str]] = {}
    
    def predict_sensation(
        self,
        motor_command: str,
        current_state: BodyState
    ) -> List[SensorimotorPattern]:
        """
        预测感觉结果
        
        前向模型: 基于运动命令预测感觉输入
        """
        predictions = []
        
        # 简化的预测
        if "reach" in motor_command:
            predictions.append(SensorimotorPattern(
                modality=SensoryModality.PROPRIOCEPTIVE,
                content="arm_extended",
                intensity=0.8,
                timestamp=0
            ))
        
        if "walk" in motor_command:
            predictions.append(SensorimotorPattern(
                modality=SensoryModality.VESTIBULAR,
                content="movement_detected",
                intensity=0.6,
                timestamp=0
            ))
        
        return predictions
    
    def compute_efference_copy(
        self,
        motor_command: str
    ) -> str:
        """
        计算感觉运动副本
        
        研究: 运动命令的内部副本用于区分自我产生和外部刺激
        """
        # 简化的副本
        return f"copy_{motor_command}_{random.randint(1000, 9999)}"


class ActivePerception:
    """
    主动感知
    
    研究: 感知是主动的,不是被动的
    """
    
    def __init__(self):
        self.attentional_focus: str = "center"
        self.scan_patterns: List[str] = []
    
    def select_attention(
        self,
        saliency_map: Dict[str, float]
    ) -> str:
        """
        选择注意力焦点
        
        基于显著性地图
        """
        if not saliency_map:
            return "center"
        
        # 选择最显著的区域
        max_saliency = max(saliency_map.values())
        
        for area, sal in saliency_map.items():
            if sal == max_saliency:
                return area
        
        return "center"
    
    def generate_scan_pattern(
        self,
        environment: Dict
    ) -> List[str]:
        """生成扫描模式"""
        patterns = []
        
        # 基于环境类型生成不同扫描
        env_type = environment.get("type", "unknown")
        
        if env_type == "social":
            patterns = ["face", "eyes", "body", "gesture"]
        elif env_type == "natural":
            patterns = ["sky", "ground", "movement", "color"]
        else:
            patterns = ["center", "left", "right", "center"]
        
        return patterns


# 示例
if __name__ == "__main__":
    # 创建具身系统
    embodied = EmbodiedCognitionSystem()
    
    # 更新身体状态
    embodied.update_body_state(
        position=(1.0, 0.0, 0.0),
        velocity=(0.5, 0.0, 0.0)
    )
    
    # 处理视觉输入
    visual = embodied.process_sensory_input(
        SensoryModality.VISUAL,
        "face_detected",
        0.9
    )
    
    print(f"Processed: {visual.modality.value} - {visual.content}")
    
    # 生成具身响应
    response = embodied.generate_embodied_response("joy", 0.8)
    print(f"Embodied response: {response}")
    
    # 获取概念具身含义
    meanings = embodied.get_grounded_meaning("happy")
    print(f"Grounded meanings: {meanings}")
