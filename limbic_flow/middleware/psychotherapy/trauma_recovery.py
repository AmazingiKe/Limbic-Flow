"""
创伤恢复模拟 - 基于研究文档实现

参考:
- TRAUMA_RECOVERY_SIMULATION.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import random
import time


class RecoveryStage(Enum):
    """恢复阶段"""
    DENIAL = "denial"
    ANGER = "anger"
    BARGAINING = "bargaining"
    DEPRESSION = "depression"
    ACCEPTANCE = "acceptance"


class InterventionType(Enum):
    """干预类型"""
    CBT = "cbt"
    EMDR = "emdr"
    DBT = "dbt"
    EXPOSURE = "exposure"


@dataclass
class TraumaMemory:
    """创伤记忆"""
    id: str
    content: str
    triggers: List[str]
    emotional_intensity: float
    activation_count: int = 0
    last_activation: float = 0.0


@dataclass
class RecoveryPlan:
    """恢复计划"""
    stage: RecoveryStage
    interventions: List[InterventionType]
    progress: float = 0.0


class TraumaMemorySystem:
    """
    创伤记忆系统
    
    研究:
    - 触发词检测
    - 闪回模拟
    - 记忆再巩固
    """
    
    def __init__(self):
        self.trauma_memories: Dict[str, TraumaMemory] = {}
        self.trigger_mappings: Dict[str, List[str]] = {}
    
    def add_trauma_memory(
        self,
        memory_id: str,
        content: str,
        triggers: List[str],
        intensity: float
    ):
        """添加创伤记忆"""
        memory = TraumaMemory(
            id=memory_id,
            content=content,
            triggers=triggers,
            emotional_intensity=intensity
        )
        
        self.trauma_memories[memory_id] = memory
        
        # 触发词映射
        for trigger in triggers:
            if trigger not in self.trigger_mappings:
                self.trigger_mappings[trigger] = []
            self.trigger_mappings[trigger].append(memory_id)
    
    def detect_trigger(self, stimulus: str) -> List[TraumaMemory]:
        """检测触发词"""
        activated = []
        
        for trigger, memory_ids in self.trigger_mappings.items():
            if trigger in stimulus:
                for memory_id in memory_ids:
                    memory = self.trauma_memories.get(memory_id)
                    if memory:
                        memory.activation_count += 1
                        memory.last_activation = time.time()
                        activated.append(memory)
        
        return activated
    
    def get_flashback_probability(self, memory_id: str) -> float:
        """获取闪回概率"""
        memory = self.trauma_memories.get(memory_id)
        
        if not memory:
            return 0.0
        
        # 基于激活次数和时间
        time_factor = min(1.0, (time.time() - memory.last_activation) / 3600)
        
        return memory.emotional_intensity * (1 + memory.activation_count) * time_factor * 0.1


class TherapeuticIntervention:
    """
    治疗干预
    
    研究:
    - CBT
    - EMDR (眼动脱敏与再处理)
    - DBT
    - 暴露疗法
    """
    
    def __init__(self):
        self.cbt = CBTTherapy()
        self.emdr = EMDRTherapy()
        self.exposure = ExposureTherapy()
    
    def apply_intervention(
        self,
        intervention_type: InterventionType,
        trauma_memory: Optional[TraumaMemory]
    ) -> Dict:
        """应用干预"""
        if intervention_type == InterventionType.CBT:
            return self.cbt.apply(trauma_memory)
        elif intervention_type == InterventionType.EMDR:
            return self.emdr.apply(trauma_memory)
        elif intervention_type == InterventionType.EXPOSURE:
            return self.exposure.apply(trauma_memory)
        
        return {"status": "unknown"}


class CBTTherapy:
    """CBT治疗"""
    
    def apply(self, memory: Optional[TraumaMemory]) -> Dict:
        if not memory:
            return {"status": "no_memory"}
        
        return {
            "technique": "cognitive_restructuring",
            "description": "识别并挑战与创伤相关的非理性信念",
            "progress_estimate": 0.2
        }


class EMDRTherapy:
    """EMDR治疗"""
    
    def apply(self, memory: Optional[TraumaMemory]) -> Dict:
        if not memory:
            return {"status": "no_memory"}
        
        return {
            "technique": "bilateral_stimulation",
            "description": "眼动脱敏,帮助加工创伤记忆",
            "progress_estimate": 0.3
        }


class ExposureTherapy:
    """暴露疗法"""
    
    def apply(self, memory: Optional[TraumaMemory]) -> Dict:
        if not memory:
            return {"status": "no_memory"}
        
        return {
            "technique": "gradual_exposure",
            "description": "逐步暴露于创伤记忆,减少恐惧",
            "progress_estimate": 0.25
        }


class ResilienceBuilder:
    """
    韧性建设
    
    研究:
    - 个人韧性因素
    - 环境韧性因素
    - 恢复轨迹
    """
    
    def __init__(self):
        self.resilience_factors = {
            "individual": ["self_efficacy", "optimism", "social_skills"],
            "environmental": ["support", "resources", "stability"]
        }
    
    def calculate_resilience(self, factors: Dict) -> float:
        """计算韧性得分"""
        score = 0.0
        
        for category in ["individual", "environmental"]:
            if category in factors:
                for factor in self.resilience_factors[category]:
                    score += factors[category].get(factor, 0.0)
        
        return min(1.0, score / len(factors))
    
    def predict_recovery_trajectory(
        self,
        resilience: float,
        intervention_quality: float
    ) -> str:
        """预测恢复轨迹"""
        combined = resilience * 0.6 + intervention_quality * 0.4
        
        if combined > 0.7:
            return "fast_recovery"
        elif combined > 0.4:
            return "gradual_recovery"
        else:
            return "slow_recovery"


class PostTraumaticGrowth:
    """
    创伤后成长
    
    研究: Tedeschi & Calhoun
    - 5个成长领域
    """
    
    GROWTH_AREAS = [
        "personal_strength",
        "new_possibilities",
        "relating_to_others",
        "appreciation_of_life",
        "spiritual_change"
    ]
    
    def __init__(self):
        self.growth_scores = {area: 0.0 for area in self.GROWTH_AREAS}
    
    def assess_growth(self, narrative: str) -> Dict[str, float]:
        """评估成长"""
        growth = {}
        
        # 简化: 基于关键词
        keywords = {
            "personal_strength": ["更强", "坚强", "成长"],
            "new_possibilities": ["新机会", "新方向", "改变"],
            "relating_to_others": ["关系", "珍惜", "关爱"],
            "appreciation_of_life": ["珍惜", "生命", "每一天"],
            "spiritual_change": ["精神", "信仰", "意义"]
        }
        
        for area, kws in keywords.items():
            count = sum(1 for kw in kws if kw in narrative)
            growth[area] = min(1.0, count * 0.2)
        
        return growth


class TraumaRecoverySimulator:
    """
    创伤恢复模拟器
    """
    
    def __init__(self):
        self.trauma_system = TraumaMemorySystem()
        self.intervention = TherapeuticIntervention()
        self.resilience = ResilienceBuilder()
        self.growth = PostTraumaticGrowth()
        self.current_stage = RecoveryStage.DENIAL
    
    def simulate(
        self,
        trauma_id: str,
        intervention: InterventionType,
        duration_days: int
    ) -> Dict:
        """模拟恢复过程"""
        memory = self.trauma_system.trauma_memories.get(trauma_id)
        
        if not memory:
            return {"error": "memory_not_found"}
        
        # 应用干预
        result = self.intervention.apply_intervention(intervention, memory)
        
        # 计算恢复进度
        daily_progress = result.get("progress_estimate", 0.1) * (duration_days / 30)
        
        # 更新阶段
        self._update_stage(daily_progress)
        
        return {
            "stage": self.current_stage.value,
            "intervention": intervention.value,
            "progress": min(1.0, daily_progress),
            "growth_assessment": self.growth.assess_growth(memory.content)
        }
    
    def _update_stage(self, progress: float):
        """更新恢复阶段"""
        if progress < 0.2:
            self.current_stage = RecoveryStage.DENIAL
        elif progress < 0.4:
            self.current_stage = RecoveryStage.ANGER
        elif progress < 0.6:
            self.current_stage = RecoveryStage.BARGAINING
        elif progress < 0.8:
            self.current_stage = RecoveryStage.DEPRESSION
        else:
            self.current_stage = RecoveryStage.ACCEPTANCE


if __name__ == "__main__":
    simulator = TraumaRecoverySimulator()
    
    # 添加创伤记忆
    simulator.trauma_system.add_trauma_memory(
        "trauma_1",
        "创伤经历...",
        ["触发词1", "触发词2"],
        0.8
    )
    
    result = simulator.simulate("trauma_1", InterventionType.CBT, 30)
    print(result)
