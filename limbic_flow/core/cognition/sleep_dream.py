"""
睡眠与梦系统 - 基于研究文档实现

参考:
- SLEEP_DREAM_CONSOLIDATION.md
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import time
import random


class SleepPhase(Enum):
    """睡眠阶段"""
    WAKE = "wake"
    NREM1 = "nrem1"
    NREM2 = "nrem2"
    NREM3 = "nrem3"
    REM = "rem"


class DreamType(Enum):
    """梦的类型"""
    EMOTIONAL_PROCESSING = "emotional"
    MEMORY_CONSOLIDATION = "memory"
    PROBLEM_SOLVING = "problem_solving"
    RANDOM = "random"


@dataclass
class SleepCycleState:
    """睡眠周期状态"""
    phase: SleepPhase
    duration_minutes: float
    memory_processing: List[str] = field(default_factory=list)


class DreamContent:
    """梦内容"""
    type: DreamType
    emotions: List[str]
    characters: List[str]
    themes: List[str]


class SleepCycleManager:
    """
    睡眠周期管理器
    
    研究:
    - NREM2: 记忆稳定化
    - NREM3: 深度整合
    - REM: 情绪处理
    """
    
    def __init__(self):
        self.current_phase = SleepPhase.WAKE
        self.cycle_count = 0
        self.phase_durations = {
            SleepPhase.NREM1: 5,
            SleepPhase.NREM2: 20,
            SleepPhase.NREM3: 20,
            SleepPhase.REM: 25,
        }
    
    def advance_phase(self) -> SleepPhase:
        """推进睡眠阶段"""
        phase_order = [
            SleepPhase.WAKE,
            SleepPhase.NREM1,
            SleepPhase.NREM2,
            SleepPhase.NREM3,
            SleepPhase.REM
        ]
        
        current_idx = phase_order.index(self.current_phase)
        
        if current_idx < len(phase_order) - 1:
            self.current_phase = phase_order[current_idx + 1]
        
        # REM后回到NREM2
        if self.current_phase == SleepPhase.REM:
            self.cycle_count += 1
        
        return self.current_phase
    
    def get_memory_processing_type(self) -> str:
        """获取当前阶段的记忆处理类型"""
        processing = {
            SleepPhase.NREM1: "light_processing",
            SleepPhase.NREM2: "memory_stabilization",
            SleepPhase.NREM3: "deep_consolidation",
            SleepPhase.REM: "emotional_processing"
        }
        
        return processing.get(self.current_phase, "none")


class DreamGenerator:
    """
    梦生成器
    
    研究:
    - 情绪梦
    - 记忆整合梦
    - 问题解决梦
    """
    
    def __init__(self):
        self.dream_themes = [
            "被追赶", "飞翔", "坠落", "考试", "迟到",
            "被困", "遇见已故亲人", "水中", "着火"
        ]
    
    def generate_dream(
        self,
        recent_memories: List[Dict],
        emotional_state: Dict
    ) -> DreamContent:
        """生成梦内容"""
        # 基于情绪生成
        emotions = self._extract_emotions(emotional_state)
        
        # 选择主题
        theme = random.choice(self.dream_themes)
        
        # 梦的类型
        dream_type = self._determine_dream_type(emotional_state)
        
        return DreamContent(
            type=dream_type,
            emotions=emotions,
            characters=[],
            themes=[theme]
        )
    
    def _extract_emotions(self, state: Dict) -> List[str]:
        """提取情绪"""
        emotions = []
        
        if state.get("pleasure", 0) > 0.3:
            emotions.append("joy")
        elif state.get("pleasure", 0) < -0.3:
            emotions.append("anxiety")
        
        if state.get("arousal", 0) > 0.7:
            emotions.append("excitement")
        
        return emotions
    
    def _determine_dream_type(self, state: Dict) -> DreamType:
        """确定梦类型"""
        if abs(state.get("pleasure", 0)) > 0.5:
            return DreamType.EMOTIONAL_PROCESSING
        elif state.get("arousal", 0) > 0.6:
            return DreamType.PROBLEM_SOLVING
        else:
            return DreamType.MEMORY_CONSOLIDATION


class SleepDreamSystem:
    """
    睡眠与梦系统
    """
    
    def __init__(self):
        self.cycle_manager = SleepCycleManager()
        self.dream_generator = DreamGenerator()
    
    def process_sleep(self, duration_hours: float) -> List[SleepCycleState]:
        """处理睡眠周期"""
        states = []
        cycles = int(duration_hours * 60 / 90)  # 90分钟周期
        
        for _ in range(cycles):
            # 进入各阶段
            for _ in range(4):  # NREM1, NREM2, NREM3, REM
                phase = self.cycle_manager.advance_phase()
                duration = self.cycle_manager.phase_durations[phase]
                
                states.append(SleepCycleState(
                    phase=phase,
                    duration_minutes=duration,
                    memory_processing=[self.cycle_manager.get_memory_processing_type()]
                ))
        
        return states
    
    def generate_dreams(self, memories: List[Dict], state: Dict) -> List[DreamContent]:
        """生成梦"""
        dreams = []
        
        for _ in range(3):  # 每晚几个梦
            dream = self.dream_generator.generate_dream(memories, state)
            dreams.append(dream)
        
        return dreams


if __name__ == "__main__":
    system = SleepDreamSystem()
    states = system.process_sleep(8)
    
    for state in states:
        print(f"{state.phase.value}: {state.memory_processing}")
