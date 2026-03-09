"""
VR情绪响应系统 - 基于研究文档实现

参考:
- VR_EMOTIONAL_RESPONSE.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import math


class ImmersionLevel(Enum):
    """沉浸级别"""
    NON_IMMERSIVE = "non_immersive"     # 2D屏幕
    SEMI_IMMERSIVE = "semi_immersive"  # 大屏环绕
    FULLY_IMMERSIVE = "fully_immersive"  # VR头显
    MIXED_REALITY = "mixed_reality"    # AR+VR


class PresenceType(Enum):
    """临场感类型"""
    SPATIAL = "spatial"        # 空间临场感
    SOCIAL = "social"          # 社会临场感
    SELF = "self"              # 自我临场感


@dataclass
class VREnvironment:
    """VR环境"""
    immersion_level: ImmersionLevel
    presence_scores: Dict[PresenceType, float] = field(default_factory=dict)
    environment_type: str = ""  # 自然/城市/恐怖/社交
    avatar_presence: bool = False


@dataclass
class VREmotionResponse:
    """VR情绪响应"""
    base_emotion: str
    presence_enhanced_intensity: float
    novelty_factor: float
    personal_relevance: float
    final_intensity: float


class VREmotionSystem:
    """
    VR情绪系统
    
    研究:
    - 沉浸谱系
    - 临场感与情绪
    - VR特定情绪
    """
    
    def __init__(self):
        self.current_environment: Optional[VREnvironment] = None
        self.presence_emotion_link = True
    
    def set_environment(self, env: VREnvironment):
        """设置VR环境"""
        self.current_environment = env
    
    def calculate_emotion(
        self,
        base_emotion: str,
        base_intensity: float,
        personal_relevance: float = 0.5
    ) -> VREmotionResponse:
        """
        计算VR环境中的情绪强度
        
        VR_Emotion = Base × Presence × Novelty × Personal_Relevance
        """
        if not self.current_environment:
            # 非VR环境
            return VREmotionResponse(
                base_emotion=base_emotion,
                presence_enhanced_intensity=base_intensity,
                novelty_factor=0.0,
                personal_relevance=personal_relevance,
                final_intensity=base_intensity
            )
        
        # 计算临场感增强
        presence_intensity = self._get_presence_intensity()
        
        # 新奇因子
        novelty = self._calculate_novelty_factor()
        
        # 最终强度
        final = (
            base_intensity * 
            presence_intensity * 
            novelty * 
            personal_relevance
        )
        
        return VREmotionResponse(
            base_emotion=base_emotion,
            presence_enhanced_intensity=presence_intensity,
            novelty_factor=novelty,
            personal_relevance=personal_relevance,
            final_intensity=min(1.0, final)
        )
    
    def _get_presence_intensity(self) -> float:
        """获取临场感强度"""
        if not self.current_environment:
            return 1.0
        
        # 平均临场感得分
        scores = self.current_environment.presence_scores.values()
        
        if not scores:
            return 1.0
        
        return sum(scores) / len(scores)
    
    def _calculate_novelty_factor(self) -> float:
        """计算新奇因子"""
        level = self.current_environment.immersion_level
        
        if level == ImmersionLevel.NON_IMMERSIVE:
            return 1.0
        elif level == ImmersionLevel.SEMI_IMMERSIVE:
            return 1.2
        elif level == ImmersionLevel.FULLY_IMMERSIVE:
            return 1.5
        else:  # MIXED_REALITY
            return 1.3


class PresenceTracker:
    """
    临场感追踪
    
    研究: 临场感与情绪双向关系
    """
    
    def __init__(self):
        self.presence_history: List[Dict] = []
        
        # 阈值
        self.high_presence_threshold = 0.7
        self.low_presence_threshold = 0.3
    
    def update_presence(
        self,
        presence_type: PresenceType,
        score: float,
        emotional_arousal: float = 0.0
    ) -> None:
        """
        更新临场感
        
        研究: 情绪增强临场感,临场感增强情绪
        """
        self.presence_history.append({
            "type": presence_type,
            "score": score,
            "arousal": emotional_arousal
        })
        
        # 反馈循环: 情绪 -> 临场感
        if emotional_arousal > 0.6:
            # 高唤醒增强临场感
            score *= 1.1
    
    def get_presence_level(self) -> float:
        """获取整体临场感水平"""
        if not self.presence_history:
            return 0.5
        
        recent = self.presence_history[-10:]
        
        return sum(p["score"] for p in recent) / len(recent)
    
    def should_enhance_emotion(self) -> bool:
        """判断是否应该增强情绪"""
        return self.get_presence_level() > self.high_presence_threshold
    
    def should_reduce_emotion(self) -> bool:
        """判断是否应该减少情绪"""
        return self.get_presence_level() < self.low_presence_threshold


class VRTherapy:
    """
    VR治疗应用
    
    研究:
    - VR暴露疗法 (VRET)
    - 生物反馈VR
    - 化身疗法
    """
    
    def __init__(self):
        self.therapy_sessions: List[Dict] = []
    
    def exposure_therapy(
        self,
        phobic_stimulus: str,
        exposure_level: float
    ) -> Dict:
        """
        VR暴露疗法
        
        逐步暴露于恐惧刺激
        """
        # 根据暴露等级计算情绪响应
        if phobic_stimulus == "heights":
            base_intensity = exposure_level * 1.5  # 恐高特别强烈
        elif phobic_stimulus == "enclosed":
            base_intensity = exposure_level * 1.2
        else:
            base_intensity = exposure_level
        
        # 治疗建议
        recommendations = []
        
        if exposure_level < 0.3:
            recommendations.append("浅层暴露,保持舒适")
        elif exposure_level < 0.7:
            recommendations.append("中等暴露,可控范围")
        else:
            recommendations.append("深层暴露,需密切监控")
        
        return {
            "stimulus": phobic_stimulus,
            "intensity": min(1.0, base_intensity),
            "recommendations": recommendations,
            "session_type": "exposure_therapy"
        }
    
    def create_calm_environment(self) -> VREnvironment:
        """创建平静环境"""
        return VREnvironment(
            immersion_level=ImmersionLevel.FULLY_IMMERSIVE,
            presence_scores={
                PresenceType.SPATIAL: 0.8,
                PresenceType.SOCIAL: 0.3,
                PresenceType.SELF: 0.7
            },
            environment_type="nature"
        )
    
    def create_social_environment(
        self,
        avatar_count: int
    ) -> VREnvironment:
        """创建社交环境"""
        return VREnvironment(
            immersion_level=ImmersionLevel.FULLY_IMMERSIVE,
            presence_scores={
                PresenceType.SPATIAL: 0.7,
                PresenceType.SOCIAL: min(1.0, avatar_count * 0.2),
                PresenceType.SELF: 0.6
            },
            environment_type="social"
        )


class BiofeedbackVR:
    """
    生物反馈VR
    
    实时生理信号影响VR环境
    """
    
    def __init__(self):
        # 生理信号
        self.heart_rate = 70
        self.gsr = 0.0  # 皮肤电反应
        self.pupil_dilation = 0.0
    
    def update_physiology(
        self,
        heart_rate: float,
        gsr: float,
        pupil: float
    ):
        """更新生理信号"""
        self.heart_rate = heart_rate
        self.gsr = gsr
        self.pupil_dilation = pupil
    
    def adjust_environment(self, environment: VREnvironment) -> VREnvironment:
        """
        根据生理信号调整环境
        
        研究: 心率、GSR、瞳孔影响VR体验
        """
        adjusted = environment
        
        # 高心率 -> 降低刺激
        if self.heart_rate > 100:
            # 调暗环境,降低声音
            adjusted.environment_type = "calm"
        
        # 高GSR -> 增强情绪响应
        if self.gsr > 0.5:
            # 情绪响应增强
            pass
        
        # 瞳孔变化 -> 调整视觉
        if self.pupil_dilation > 0.7:
            # 增强视觉细节
            pass
        
        return adjusted


# 示例
if __name__ == "__main__":
    # 创建VR系统
    vr_system = VREmotionSystem()
    
    # 设置沉浸环境
    env = VREnvironment(
        immersion_level=ImmersionLevel.FULLY_IMMERSIVE,
        presence_scores={
            PresenceType.SPATIAL: 0.8,
            PresenceType.SOCIAL: 0.5,
            PresenceType.SELF: 0.7
        },
        environment_type="nature"
    )
    
    vr_system.set_environment(env)
    
    # 计算情绪
    response = vr_system.calculate_emotion(
        "joy",
        0.6,
        personal_relevance=0.8
    )
    
    print(f"Base: 0.6, Final: {response.final_intensity:.2f}")
    
    # VR治疗
    therapy = VRTherapy()
    result = therapy.exposure_therapy("heights", 0.5)
    print(f"Therapy: {result}")
