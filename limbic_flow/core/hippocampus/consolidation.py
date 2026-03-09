"""
记忆巩固系统 - 基于研究文档实现

参考:
- MEMORY_CONSOLIDATION_ALGORITHMS.md
- SLEEP_DREAM_CONSOLIDATION.md
- MEMORY_FORGETTING_MECHANISMS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math
import time
import random
import numpy as np


class SleepStage(Enum):
    """睡眠阶段"""
    AWAKE = "awake"
    NREM_1 = "nrem1"      # 浅睡眠
    NREM_2 = "nrem2"      # 睡眠锭阶段
    NREM_3 = "nrem3"      # 深度睡眠
    REM = "rem"           # 快速眼动睡眠


@dataclass
class Memory:
    """记忆结构"""
    id: str
    content: str
    vector: np.ndarray
    emotional_tags: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    importance: float = 0.5  # 重要性
    access_count: int = 0
    
    # 巩固相关
    consolidation_level: float = 0.0  # 0=新记忆, 1=完全巩固
    replay_count: int = 0


@dataclass
class SleepCycle:
    """睡眠周期"""
    stage: SleepStage
    duration_minutes: float = 0.0
    
    # 各阶段特征
    memory_processing = {
        SleepStage.AWAKE: "encoding",
        SleepStage.NREM_1: "light_processing",
        SleepStage.NREM_2: "memory_stabilization",
        SleepStage.NREM_3: "deep_consolidation",
        SleepStage.REM: "emotional_processing",
    }


class MemoryConsolidation:
    """
    记忆巩固系统
    
    研究参考:
    - 海马体-新皮层记忆巩固
    - 睡眠依赖的记忆巩固
    - 记忆重播 (Memory Replay)
    """
    
    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.pending_consolidation: List[str] = []  # 待巩固的记忆
        self.replay_queue: List[str] = []  # 重播队列
        
        # 巩固参数
        self.consolidation_threshold = 0.7  # 需要巩固的阈值
        self.replay_priority_weight = {
            "emotional": 0.4,
            "importance": 0.3,
            "recency": 0.2,
            "novelty": 0.1,
        }
    
    def register_memory(self, memory: Memory) -> None:
        """注册新记忆"""
        self.memories[memory.id] = memory
        self.pending_consolidation.append(memory.id)
    
    def get_consolidation_priority(self, memory_id: str) -> float:
        """
        计算记忆的巩固优先级
        
        基于:
        - 情绪强度
        - 重要性
        - 新近度
        - 新颖性
        """
        if memory_id not in self.memories:
            return 0.0
        
        memory = self.memories[memory_id]
        
        # 情绪强度
        emotional_intensity = sum(abs(v) for v in memory.emotional_tags.values())
        emotional_score = min(1.0, emotional_intensity)
        
        # 重要性
        importance_score = memory.importance
        
        # 新近度 (越新越需要巩固)
        age_hours = (time.time() - memory.timestamp) / 3600
        recency_score = math.exp(-age_hours / 24)  # 24小时半衰期
        
        # 新颖性 (访问次数少 = 新颖)
        novelty_score = 1.0 / (1.0 + memory.access_count)
        
        # 综合得分
        priority = (
            emotional_score * self.replay_priority_weight["emotional"] +
            importance_score * self.replay_priority_weight["importance"] +
            recency_score * self.replay_priority_weight["recency"] +
            novelty_score * self.replay_priority_weight["novelty"]
        )
        
        return priority
    
    def process_during_sleep(self, sleep_stage: SleepStage, duration_minutes: float) -> List[str]:
        """
        睡眠期间处理记忆
        
        Args:
            sleep_stage: 当前睡眠阶段
            duration_minutes: 持续时间
        
        Returns:
            List[str]: 处理过的记忆ID列表
        """
        processed = []
        
        if sleep_stage == SleepStage.NREM_2:
            # NREM_2: 记忆稳定化
            processed = self._stabilize_memories(duration_minutes)
        
        elif sleep_stage == SleepStage.NREM_3:
            # NREM_3: 深度巩固
            processed = self._deep_consolidate(duration_minutes)
        
        elif sleep_stage == SleepStage.REM:
            # REM: 情绪处理和记忆整合
            processed = self._process_emotional_memories(duration_minutes)
        
        return processed
    
    def _stabilize_memories(self, duration_minutes: float) -> List[str]:
        """NREM_2: 记忆稳定化"""
        processed = []
        
        # 选择需要巩固的记忆
        candidates = self._select_candidates_for_consolidation(10)
        
        for memory_id in candidates:
            memory = self.memories[memory_id]
            
            # 增加巩固水平
            consolidation_gain = duration_minutes * 0.02  # 每分钟2%
            memory.consolidation_level = min(1.0, memory.consolidation_level + consolidation_gain)
            
            processed.append(memory_id)
        
        return processed
    
    def _deep_consolidate(self, duration_minutes: float) -> List[str]:
        """NREM_3: 深度巩固 - 记忆转移到长期存储"""
        processed = []
        
        # 选择完全巩固的记忆
        candidates = [m for m in self.memories.values() 
                      if m.consolidation_level >= self.consolidation_threshold]
        
        for memory in candidates:
            # 标记为长期记忆
            memory.consolidation_level = 1.0
            processed.append(memory.id)
        
        return processed
    
    def _process_emotional_memories(self, duration_minutes: float) -> List[str]:
        """REM: 情绪记忆处理"""
        processed = []
        
        # 选择情绪记忆优先处理
        emotional_candidates = [
            m for m in self.memories.values()
            if sum(abs(v) for v in m.emotional_tags.values()) > 0.3
        ]
        
        # 按情绪强度排序
        emotional_candidates.sort(
            key=lambda m: sum(abs(v) for v in m.emotional_tags.values()),
            reverse=True
        )
        
        # 处理前几个
        for memory in emotional_candidates[:5]:
            # 增强情绪标签
            for tag, value in memory.emotional_tags.items():
                memory.emotional_tags[tag] = value * 1.05  # 轻微增强
            
            memory.replay_count += 1
            processed.append(memory.id)
        
        return processed
    
    def _select_candidates_for_consolidation(self, limit: int) -> List[str]:
        """选择待巩固的记忆"""
        candidates = []
        
        for memory_id in self.pending_consolidation:
            if memory_id in self.memories:
                priority = self.get_consolidation_priority(memory_id)
                candidates.append((priority, memory_id))
        
        # 按优先级排序
        candidates.sort(key=lambda x: x[0], reverse=True)
        
        return [m[1] for m in candidates[:limit]]
    
    def trigger_replay(self, memory_id: str) -> Optional[str]:
        """
        触发记忆重播
        
        研究: 记忆重播是巩固的关键机制
        """
        if memory_id not in self.memories:
            return None
        
        memory = self.memories[memory_id]
        memory.replay_count += 1
        
        # 重播增加巩固
        memory.consolidation_level = min(1.0, memory.consolidation_level + 0.05)
        
        return f"Replaying memory {memory_id}: {memory.content[:50]}..."


class ForgettingMechanisms:
    """
    遗忘机制
    
    研究参考:
    - 自然衰减
    - 抑制性遗忘
    - 适应性遗忘
    """
    
    def __init__(self):
        # 遗忘参数
        self.base_decay_rate = 0.01  # 基础衰减率
        self.emotional_protection = 0.3  # 情绪记忆保护因子
    
    def calculate_forgetting(
        self, 
        memory: Memory, 
        elapsed_hours: float,
        current_mood: Optional[Dict[str, float]] = None
    ) -> float:
        """
        计算记忆的遗忘率
        
        Args:
            memory: 记忆
            elapsed_hours: 经过的小时数
            current_mood: 当前情绪状态
        
        Returns:
            float: 遗忘概率 [0-1]
        """
        # 基础遗忘 (Ebbinghaus 曲线)
        base_forgetting = 1.0 - math.exp(-self.base_decay_rate * elapsed_hours / 24)
        
        # 情绪保护
        emotional_intensity = sum(abs(v) for v in memory.emotional_tags.values())
        protection_factor = 1.0 - (emotional_intensity * self.emotional_protection)
        
        # 当前情绪影响
        mood_modifier = 1.0
        if current_mood:
            # 抑郁状态: 负面记忆更难遗忘
            if current_mood.get("pleasure", 0) < -0.3:
                # 增强负面记忆
                if memory.emotional_tags.get("negative", 0) > 0.5:
                    mood_modifier = 0.7
        
        final_forgetting = base_forgetting * protection_factor * mood_modifier
        
        return min(1.0, final_forgetting)
    
    def should_forget(self, memory: Memory, current_mood: Optional[Dict] = None) -> bool:
        """判断是否应该遗忘"""
        elapsed_hours = (time.time() - memory.timestamp) / 3600
        
        forgetting_prob = self.calculate_forgetting(memory, elapsed_hours, current_mood)
        
        return random.random() < forgetting_prob


class SleepCycleSimulator:
    """
    睡眠周期模拟器
    
    研究: 睡眠周期影响记忆巩固类型
    - NREM_2: 记忆稳定
    - NREM_3: 深度整合
    - REM: 情绪处理
    """
    
    def __init__(self):
        self.current_stage = SleepStage.AWAKE
        self.cycle_duration_minutes = 90  # 典型睡眠周期90分钟
        self.stage_durations = {
            SleepStage.NREM_1: 5,
            SleepStage.NREM_2: 20,
            SleepStage.NREM_3: 20,
            SleepStage.REM: 25,
            SleepStage.AWAKE: 20,  # 入睡时间
        }
    
    def simulate_cycle(self) -> List[Tuple[SleepStage, float]]:
        """
        模拟一个睡眠周期
        
        Returns:
            List[Tuple[SleepStage, float]]: (阶段, 持续时间) 列表
        """
        cycle = []
        
        # 入睡
        cycle.append((SleepStage.AWAKE, self.stage_durations[SleepStage.AWAKE]))
        
        # NREM 循环 (通常4-5个周期)
        for i in range(4):
            cycle.append((SleepStage.NREM_1, self.stage_durations[SleepStage.NREM_1]))
            cycle.append((SleepStage.NREM_2, self.stage_durations[SleepStage.NREM_2]))
            cycle.append((SleepStage.NREM_3, self.stage_durations[SleepStage.NREM_3]))
            
            # REM 时间随周期增加
            rem_duration = self.stage_durations[SleepStage.REM] + (i * 5)
            cycle.append((SleepStage.REM, rem_duration))
        
        return cycle
    
    def get_stage_for_minute(self, minute: int) -> SleepStage:
        """获取指定分钟的睡眠阶段"""
        cycle = self.simulate_cycle()
        
        elapsed = 0
        for stage, duration in cycle:
            elapsed += duration
            if minute < elapsed:
                return stage
        
        return SleepStage.AWAKE


# 示例
if __name__ == "__main__":
    # 创建记忆
    memory = Memory(
        id="mem_001",
        content="今天学到了新的知识",
        vector=np.random.rand(10),
        emotional_tags={"joy": 0.8, "interest": 0.6},
        importance=0.7
    )
    
    # 创建巩固系统
    consolidation = MemoryConsolidation()
    consolidation.register_memory(memory)
    
    # 模拟睡眠处理
    results = consolidation.process_during_sleep(SleepStage.REM, 25)
    print(f"Processed memories: {results}")
    
    # 遗忘机制
    forgetting = ForgettingMechanisms()
    elapsed = 24 * 3  # 3天后
    forget_prob = forgetting.calculate_forget(memory, elapsed)
    print(f"Forgetting probability after 3 days: {forget_prob:.2%}")
