"""
情感记忆标记系统 - 基于研究文档实现

参考:
- EMOTION_REGULATION_ALGORITHMS.md
- MEMORY_MANAGEMENT_RESEARCH.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import time
import numpy as np


class MemoryTagType(Enum):
    """记忆标签类型"""
    EMOTION = "emotion"           # 情绪标签
    VALENCE = "valence"          # 效价 (正/负)
    AROUSAL = "arousal"          # 唤醒度
    EVENT = "event"              # 事件类型
    PERSON = "person"            # 人物
    LOCATION = "location"        # 地点
    TIME = "time"                # 时间
    TRAUMA = "trauma"            # 创伤标记
    PLEASURE = "pleasure"        # 愉悦度


@dataclass
class EmotionalTag:
    """情感标签"""
    tag_type: MemoryTagType
    value: float                 # 值 [-1, 1] 或 [0, 1]
    confidence: float = 0.8      # 置信度
    timestamp: float = field(default_factory=time.time)


@dataclass
class TaggedMemory:
    """带情感标签的记忆"""
    id: str
    content: str
    vector: np.ndarray
    emotional_tags: List[EmotionalTag] = field(default_factory=list)
    salience: float = 0.5        # 显著度
    timestamp: float = field(default_factory=time.time)


class EmotionalTagger:
    """
    情感标签器
    
    研究: amygdala-hippocampus binding
    - 情绪增强记忆编码
    - 记忆的情绪标签影响检索
    """
    
    def __init__(self):
        # 基础情感词典
        self.emotion_lexicon = {
            "joy": {"valence": 0.8, "arousal": 0.6},
            "happiness": {"valence": 0.8, "arousal": 0.5},
            "sadness": {"valence": -0.7, "arousal": 0.4},
            "anger": {"valence": -0.6, "arousal": 0.8},
            "fear": {"valence": -0.7, "arousal": 0.9},
            "surprise": {"valence": 0.0, "arousal": 0.8},
            "disgust": {"valence": -0.6, "arousal": 0.5},
            "love": {"valence": 0.8, "arousal": 0.5},
            "hope": {"valence": 0.6, "arousal": 0.4},
            "anxiety": {"valence": -0.5, "arousal": 0.7},
            "guilt": {"valence": -0.5, "arousal": 0.5},
            "shame": {"valence": -0.5, "arousal": 0.5},
        }
        
        # 创伤词
        self.trauma_triggers = [
            "死亡", "失去", "创伤", "车祸", "事故",
            "暴力", "虐待", "伤害", "恐惧", "害怕"
        ]
    
    def tag_memory(
        self, 
        content: str, 
        vector: np.ndarray,
        detected_emotions: Optional[List[str]] = None
    ) -> TaggedMemory:
        """
        为记忆添加情感标签
        
        Args:
            content: 记忆内容
            vector: 记忆向量
            detected_emotions: 检测到的情绪词
        
        Returns:
            TaggedMemory: 带标签的记忆
        """
        memory_id = f"mem_{int(time.time() * 1000)}"
        
        # 自动检测情绪词
        if detected_emotions is None:
            detected_emotions = self._detect_emotions(content)
        
        # 创建情感标签
        tags = []
        
        # 1. 检测效价和唤醒度
        if detected_emotions:
            for emotion in detected_emotions:
                if emotion in self.emotion_lexicon:
                    lexicon_entry = self.emotion_lexicon[emotion]
                    
                    tags.append(EmotionalTag(
                        tag_type=MemoryTagType.VALENCE,
                        value=lexicon_entry["valence"],
                        confidence=0.9
                    ))
                    
                    tags.append(EmotionalTag(
                        tag_type=MemoryTagType.AROUSAL,
                        value=lexicon_entry["arousal"],
                        confidence=0.9
                    ))
        
        # 2. 检测效价 (如果没有检测到情绪)
        if not tags:
            valence = self._estimate_valence(content)
            tags.append(EmotionalTag(
                tag_type=MemoryTagType.VALENCE,
                value=valence,
                confidence=0.6
            ))
        
        # 3. 检测创伤标记
        if self._has_trauma_content(content):
            tags.append(EmotionalTag(
                tag_type=MemoryTagType.TRAUMA,
                value=1.0,
                confidence=0.8
            ))
        
        # 4. 计算显著度
        salience = self._calculate_salience(tags, content)
        
        return TaggedMemory(
            id=memory_id,
            content=content,
            vector=vector,
            emotional_tags=tags,
            salience=salience,
            timestamp=time.time()
        )
    
    def _detect_emotions(self, text: str) -> List[str]:
        """检测文本中的情绪词"""
        text_lower = text.lower()
        detected = []
        
        for emotion in self.emotion_lexicon:
            if emotion in text_lower:
                detected.append(emotion)
        
        return detected
    
    def _estimate_valence(self, text: str) -> float:
        """估计文本效价"""
        positive_words = ["好", "喜欢", "开心", "棒", "优秀", "成功", "快乐"]
        negative_words = ["坏", "讨厌", "难过", "差", "失败", "痛苦", "悲伤"]
        
        score = 0.0
        
        for word in positive_words:
            if word in text:
                score += 0.2
        
        for word in negative_words:
            if word in text:
                score -= 0.2
        
        return max(-1.0, min(1.0, score))
    
    def _has_trauma_content(self, text: str) -> bool:
        """检查是否有创伤内容"""
        for trigger in self.trauma_triggers:
            if trigger in text:
                return True
        return False
    
    def _calculate_salience(self, tags: List[EmotionalTag], content: str) -> float:
        """计算记忆显著度"""
        salience = 0.5
        
        # 情绪强度影响显著度
        for tag in tags:
            if tag.tag_type == MemoryTagType.TRAUMA:
                salience += 0.3
            elif tag.tag_type == MemoryTagType.VALENCE:
                salience += abs(tag.value) * 0.2
        
        # 内容长度
        if len(content) > 100:
            salience += 0.1
        elif len(content) > 50:
            salience += 0.05
        
        return min(1.0, salience)


class MoodCongruentRetrieval:
    """
    情绪一致性检索
    
    研究: 抑郁状态 -> 更容易检索负面记忆
    """
    
    def __init__(self):
        self.current_mood = {
            "pleasure": 0.0,
            "arousal": 0.5,
            "dominance": 0.5
        }
    
    def set_mood(self, mood: Dict[str, float]):
        """设置当前情绪"""
        self.current_mood = mood
    
    def filter_memories(
        self, 
        memories: List[TaggedMemory],
        bias_strength: float = 0.5
    ) -> List[TaggedMemory]:
        """
        过滤记忆 - 情绪一致性偏差
        
        研究: 情绪状态影响记忆检索
        - 抑郁: 负面记忆更容易被检索
        - 开心: 正面记忆更容易被检索
        """
        if bias_strength == 0:
            return memories
        
        mood_valence = self.current_mood.get("pleasure", 0.0)
        
        scored_memories = []
        
        for memory in memories:
            # 获取记忆的情绪值
            memory_valence = 0.0
            for tag in memory.emotional_tags:
                if tag.tag_type == MemoryTagType.VALENCE:
                    memory_valence = tag.value
                    break
            
            # 计算一致性
            # 情绪一致 -> 增强检索
            # 情绪不一致 -> 抑制检索
            congruence = 1.0 - abs(mood_valence - memory_valence) / 2.0
            
            # 应用偏差
            bias_factor = 1.0 + (congruence - 0.5) * bias_strength
            
            score = memory.salience * bias_factor
            scored_memories.append((score, memory))
        
        # 按得分排序
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        return [m for _, m in scored_memories]


class MemoryReconsolidation:
    """
    记忆再巩固
    
    研究: 记忆被提取后可以修改
    - 激活 -> 提取 -> 再巩固 -> 存储
    """
    
    def __init__(self):
        self.reconsolidation_window = 6 * 3600  # 6小时
    
    def should_reconsolidate(
        self, 
        last_accessed: float,
        current_emotion: float
    ) -> bool:
        """
        判断是否需要再巩固
        
        Args:
            last_accessed: 上次访问时间
            current_emotion: 当前情绪状态
        """
        time_since = time.time() - last_accessed
        
        # 在窗口期内且情绪强烈
        if time_since < self.reconsolidation_window:
            if abs(current_emotion) > 0.5:
                return True
        
        return False
    
    def update_memory(
        self, 
        memory: TaggedMemory, 
        new_emotion: float
    ) -> TaggedMemory:
        """
        更新记忆的情感标签
        
        再巩固期间可以修改记忆
        """
        # 添加新的情绪标签
        memory.emotional_tags.append(EmotionalTag(
            tag_type=MemoryTagType.EMOTION,
            value=new_emotion,
            confidence=0.7,
            timestamp=time.time()
        ))
        
        # 重新计算显著度
        memory.salience = min(1.0, memory.salience * 1.1)
        
        return memory


# 示例
if __name__ == "__main__":
    # 创建标签器
    tagger = EmotionalTagger()
    
    # 标记记忆
    memory = tagger.tag_memory(
        content="今天得到了一个好消息,我很高兴!",
        vector=np.random.rand(10),
        detected_emotions=["happiness", "joy"]
    )
    
    print(f"Memory ID: {memory.id}")
    print(f"Salience: {memory.salience}")
    print("Tags:")
    for tag in memory.emotional_tags:
        print(f"  {tag.tag_type.value}: {tag.value}")
    
    # 测试情绪一致性检索
    retrieval = MoodCongruentRetrieval()
    retrieval.set_mood({"pleasure": -0.5, "arousal": 0.6, "dominance": 0.4})
    
    # 模拟记忆列表
    memories = [
        TaggedMemory("1", "好事", np.random.rand(10), [
            EmotionalTag(MemoryTagType.VALENCE, 0.8)
        ], 0.7),
        TaggedMemory("2", "坏事", np.random.rand(10), [
            EmotionalTag(MemoryTagType.VALENCE, -0.8)
        ], 0.7),
    ]
    
    filtered = retrieval.filter_memories(memories, bias_strength=0.7)
    print("\nFiltered memories (sad mood):")
    for m in filtered:
        print(f"  {m.content}")
