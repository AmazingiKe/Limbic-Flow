"""
扩展病理模块 - 基于研究文档实现

参考:
- DEPRESSION_MODELING.md
- BIPOLAR_DISORDER_SIMULATION.md
- ANXIETY_DISORDER_MODELING.md
- AUTISM_ADHD_MODELING.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import math
import time
import random


class PathologyType(Enum):
    """病理类型"""
    DEPRESSION = "depression"
    BIPOLAR = "bipolar"
    ANXIETY = "anxiety"
    PTSD = "ptsd"
    ALZHEIMER = "alzheimer"
    AUTISM = "autism"
    ADHD = "adhd"


@dataclass
class PathologyState:
    """病理状态"""
    active: bool = False
    severity: float = 0.5  # 0-1
    triggers: List[str] = field(default_factory=list)
    last_episode: float = 0.0


class DepressionPathology:
    """
    抑郁病理模块
    
    研究参考:
    - 快感缺失 (Anhedonia)
    - 负性偏见 (Negative Bias)
    - 反刍思维 (Rumination)
    - 睡眠-能量耦合
    """
    
    def __init__(self, severity: float = 0.5):
        self.severity = severity
        self.state = PathologyState(active=False, severity=severity)
        
        # 抑郁参数
        self.anhedonia_threshold = 0.3
        self.negative_bias_strength = 0.4
        self.rumination_threshold = 0.6
        self.positive_memory_attenuation = 0.3
    
    def activate(self):
        """激活抑郁模式"""
        self.state.active = True
        self.state.last_episode = time.time()
    
    def deactivate(self):
        """关闭抑郁模式"""
        self.state.active = False
    
    def apply(self, pad: Dict[str, float], context: str = "") -> Dict[str, float]:
        """
        应用抑郁病理影响
        
        Args:
            pad: 当前PAD状态
            context: 上下文
        
        Returns:
            Dict: 修改后的PAD
        """
        if not self.state.active:
            return pad
        
        result = pad.copy()
        
        # 1. 快感缺失 - 降低愉悦感
        if result["pleasure"] > 0:
            # 正面情绪被衰减
            result["pleasure"] *= (1.0 - self.severity * self.anhedonia_threshold)
        
        # 2. 负性偏见 - 增强负面情绪
        if result["pleasure"] < 0:
            result["pleasure"] -= self.severity * self.negative_bias_strength
            result["pleasure"] = max(-1.0, result["pleasure"])
        
        # 3. 反刍 - 增加唤醒度
        if abs(result["pleasure"]) > self.rumination_threshold:
            result["arousal"] = min(1.0, result["arousal"] + self.severity * 0.2)
        
        # 4. 降低掌控感
        result["dominance"] = max(0.0, result["dominance"] - self.severity * 0.2)
        
        return result
    
    def filter_memories(self, memories: List[Dict]) -> List[Dict]:
        """
        过滤记忆 - 抑郁状态下正面记忆被抑制
        
        研究: 抑郁状态下的情绪一致性记忆偏差
        """
        if not self.state.active:
            return memories
        
        filtered = []
        for mem in memories:
            pad = mem.get("pad", {})
            pleasure = pad.get("pleasure", 0.0)
            
            # 正面记忆被衰减
            if pleasure > 0:
                # 根据严重程度衰减
                if random.random() > self.severity * self.positive_memory_attenuation:
                    filtered.append(mem)
            else:
                # 负面记忆保留
                filtered.append(mem)
        
        return filtered
    
    def calculate_severity(self, pad: Dict[str, float]) -> float:
        """根据当前状态计算抑郁严重程度"""
        score = 0.0
        
        # 低愉悦度
        if pad.get("pleasure", 0) < 0:
            score += abs(pad["pleasure"]) * 0.3
        
        # 低掌控感
        if pad.get("dominance", 0.5) < 0.3:
            score += (0.3 - pad["dominance"]) * 0.3
        
        # 高唤醒但低愉悦 (可能是反刍)
        if pad.get("arousal", 0) > 0.6 and pad.get("pleasure", 0) < 0:
            score += 0.2
        
        return min(1.0, score)


class BipolarPathology:
    """
    双相情感障碍模块
    
    研究参考:
    - 躁郁循环
    - 躁狂: 奖励敏感度升高、决断力下降
    - 抑郁: 同抑郁模块
    """
    
    def __init__(self):
        self.state = PathologyState(active=False, severity=0.5)
        
        # 参数
        self.cycle_period_hours = 24 * 7  # 默认7天周期
        self.mania_threshold = 0.7
        self.depression_threshold = -0.3
        
        # 状态
        self.current_polarity = "euthymic"  # mania/hypomania/depression/euthymic
        self.cycle_progress = 0.0
        
        # 躁狂参数
        self.mania_reward_sensitivity = 1.5
        self.mania_deliberation_cost = 0.3
    
    def activate(self, severity: float = 0.5):
        """激活双相模式"""
        self.state.active = True
        self.state.severity = severity
        self.state.last_episode = time.time()
    
    def update_cycle(self, elapsed_hours: float) -> str:
        """
        更新循环状态
        
        Returns:
            str: 当前极性 (mania/hypomania/depression/euthymic)
        """
        if not self.state.active:
            return "euthymic"
        
        # 计算周期进度
        self.cycle_progress = (elapsed_hours % self.cycle_period_hours) / self.cycle_period_hours
        
        # 使用正弦函数模拟情绪循环
        mood_value = math.sin(self.cycle_progress * 2 * math.pi)
        
        if mood_value > self.mania_threshold:
            self.current_polarity = "mania"
        elif mood_value > 0.2:
            self.current_polarity = "hypomania"
        elif mood_value < self.depression_threshold:
            self.current_polarity = "depression"
        else:
            self.current_polarity = "euthymic"
        
        return self.current_polarity
    
    def apply(self, pad: Dict[str, float]) -> Dict[str, float]:
        """应用双相病理影响"""
        if not self.state.active:
            return pad
        
        polarity = self.update_cycle(time.time() - self.state.last_episode)
        
        result = pad.copy()
        
        if polarity == "mania" or polarity == "hypomania":
            # 躁狂状态
            # 1. 奖励敏感度升高
            if result["pleasure"] > 0:
                result["pleasure"] = min(1.0, result["pleasure"] * self.mania_reward_sensitivity)
            
            # 2. 唤醒度升高
            result["arousal"] = min(1.0, result["arousal"] + self.severity * 0.3)
            
            # 3. 决断力变化
            result["dominance"] = min(1.0, result["dominance"] + self.severity * 0.2)
        
        elif polarity == "depression":
            # 抑郁状态 - 使用抑郁模块
            depression = DepressionPathology(self.state.severity)
            depression.activate()
            result = depression.apply(result)
        
        return result
    
    def get_cycle_info(self) -> Dict:
        """获取循环信息"""
        return {
            "polarity": self.current_polarity,
            "progress": self.cycle_progress,
            "period_hours": self.cycle_period_hours,
        }


class AnxietyPathology:
    """
    焦虑障碍模块
    
    研究参考:
    - 广泛性焦虑
    - 担忧反刍
    - 回避行为
    - 生理唤醒增强
    """
    
    def __init__(self):
        self.state = PathologyState(active=False, severity=0.5)
        
        # 参数
        self.baseline_cortisol_boost = 0.3
        self.threat_sensitivity = 2.0
        self.worry_threshold = 0.5
        self.avoidance_threshold = 0.7
    
    def activate(self, severity: float = 0.5):
        """激活焦虑模式"""
        self.state.active = True
        self.state.severity = severity
    
    def apply(self, pad: Dict[str, float], context: str = "") -> Dict[str, float]:
        """应用焦虑病理影响"""
        if not self.state.active:
            return pad
        
        result = pad.copy()
        
        # 1. 唤醒度升高
        result["arousal"] = min(1.0, result["arousal"] + self.severity * 0.3)
        
        # 2. 愉悦度降低
        if result["pleasure"] > 0:
            result["pleasure"] *= (1.0 - self.severity * 0.2)
        
        # 3. 掌控感降低
        result["dominance"] = max(0.0, result["dominence"] - self.severity * 0.2)
        
        # 4. 检测威胁词触发担忧
        threat_words = ["失败", "错误", "危险", "担心", "焦虑"]
        for word in threat_words:
            if word in context:
                # 触发担忧
                result["arousal"] = min(1.0, result["arousal"] + self.severity * 0.2)
                break
        
        return result
    
    def should_avoid(self, context: str) -> bool:
        """判断是否应该回避"""
        if not self.state.active:
            return False
        
        threat_words = ["考试", "演讲", "面试", "公开"]
        for word in threat_words:
            if word in context:
                return random.random() < (self.severity * self.avoidance_threshold)
        
        return False


class PathologyManager:
    """
    病理管理器
    
    统一管理所有病理模块
    """
    
    def __init__(self):
        self.pathologies: Dict[PathologyType, object] = {
            PathologyType.DEPRESSION: DepressionPathology(),
            PathologyType.BIPOLAR: BipolarPathology(),
            PathologyType.ANXIETY: AnxietyPathology(),
        }
    
    def enable(self, pathology_type: PathologyType, severity: float = 0.5):
        """启用病理"""
        if pathology_type in self.pathologies:
            pathology = self.pathologies[pathology_type]
            if hasattr(pathology, 'activate'):
                pathology.activate(severity)
            elif hasattr(pathology, 'state'):
                pathology.state.active = True
                pathology.state.severity = severity
    
    def disable(self, pathology_type: PathologyType):
        """禁用病理"""
        if pathology_type in self.pathologies:
            pathology = self.pathologies[pathology_type]
            if hasattr(pathology, 'deactivate'):
                pathology.deactivate()
            elif hasattr(pathology, 'state'):
                pathology.state.active = False
    
    def apply_all(self, pad: Dict[str, float], context: str = "") -> Dict[str, float]:
        """应用所有活跃病理"""
        result = pad.copy()
        
        for pathology in self.pathologies.values():
            if hasattr(pathology, 'state') and pathology.state.active:
                if hasattr(pathology, 'apply'):
                    result = pathology.apply(result, context)
        
        return result


# 示例
if __name__ == "__main__":
    # 测试抑郁模块
    depression = DepressionPathology(severity=0.7)
    depression.activate()
    
    test_pad = {"pleasure": 0.8, "arousal": 0.5, "dominance": 0.6}
    result = depression.apply(test_pad)
    print(f"Original: {test_pad}")
    print(f"Depressed: {result}")
    
    # 测试双相模块
    bipolar = BipolarPathology()
    bipolar.activate(severity=0.6)
    
    print(f"\nBipolar cycle: {bipolar.get_cycle_info()}")
