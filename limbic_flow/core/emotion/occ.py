"""
OCC 情感模型 - 基于认知评估的情绪模型

OCC (Ortony, Clore, Collins) 模型:
- 根据事件、行为、对象的评估结果产生情绪
- 22种基本情绪类型
- 更符合人类认知过程

与 PAD 的区别:
- PAD: 维度模型 (愉悦度/唤醒度/控制度)
- OCC: 认知评估模型 (事件评估 → 情绪类型)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import math


class OCCEmotion(Enum):
    """
    OCC 情绪类型 (22种)
    
    根据评估对象分为三类:
    - 事件结果 (Consequences of events)
    - 代理行为 (Actions of agents)  
    - 对象方面 (Aspects of objects)
    """
    # 正面结果 (Prospect-based)
    HOPE = "hope"           # 希望
    SATISFACTION = "satisfaction"  # 满意
    RELIEF = "relief"       # 宽慰
    JOY = "joy"             # 喜悦
    DISAPPOINTMENT = "disappointment"  # 失望
    FEAR_CONFOUNDING = "fear_confounding"  # 恐惧
    
    # 确认/否认 (Confirmation)
    SATISFACTION_CONFIRM = "satisfaction_confirm"  # 确认满意
    DISAPPOINTMENT_DISCONFIRM = "disappointment_disconfirm"  # 否认失望
    
    # 代理行为 - 他人 (Other's actions)
    PRIDE = "pride"         # 自豪
    SHAME = "shame"         # 羞耻
    ADMIRATION = "admiration"  # 钦佩
    REPROACH = "reproach"   # 责备
    
    # 代理行为 - 自己 (Self actions)
    SELF_PRIDE = "self_pride"     # 自我自豪
    SELF_SHAME = "self_shame"    # 自我羞耻
    
    # 对象 - 吸引 (Attraction)
    LOVE = "love"           # 爱
    HATE = "hate"          # 恨
    
    # 复合情绪
    GRATITUDE = "gratitude"    # 感激
    ANGER = "anger"         # 愤怒
    FEAR = "fear"           # 害怕
    DISTRESS = "distress"   # 苦恼
    HAPPINESS = "happiness" # 幸福
    SADNESS = "sadness"     # 悲伤


@dataclass
class Appraisal:
    """
    认知评估结果
    
    OCC 模型的核心：评估决定情绪
    """
    # 事件评估
    desirability: float = 0.0     # 期望程度 [-1, 1]
    desirability_for_other: float = 0.0  # 对他人的期望
    praiseworthiness: float = 0.0   # 值不值得称赞 [-1, 1]
    attractiveness: float = 0.0    # 吸引力 [-1, 1]
    
    # 评估维度
    likelihood: float = 0.5        # 可能性 [0, 1]
    expectedness: float = 0.5     # 预期性 [0, 1]
    
    # 因果归因
    causal_attribution_self: float = 0.0   # 归因自己 [-1, 1]
    causal_attribution_other: float = 0.0   # 归因他人 [-1, 1]
    
    # 结果
    realized: bool = True           # 是否已发生
    goal_relevant: bool = True      # 与目标相关


@dataclass 
class OCCState:
    """
    OCC 情绪状态
    
    每种情绪的强度值 [0, 1]
    """
    # 主要情绪
    hope: float = 0.0
    joy: float = 0.0
    satisfaction: float = 0.0
    relief: float = 0.0
    disappointment: float = 0.0
    fear: float = 0.0
    
    # 自我情绪
    pride: float = 0.0
    shame: float = 0.0
    self_pride: float = 0.0
    self_shame: float = 0.0
    
    # 他人情绪
    admiration: float = 0.0
    reproach: float = 0.0
    gratitude: float = 0.0
    anger: float = 0.0
    
    # 复合情绪
    love: float = 0.0
    hate: float = 0.0
    distress: float = 0.0
    sadness: float = 0.0
    happiness: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "hope": self.hope, "joy": self.joy, "satisfaction": self.satisfaction,
            "relief": self.relief, "disappointment": self.disappointment, "fear": self.fear,
            "pride": self.pride, "shame": self.shame, "self_pride": self.self_pride,
            "self_shame": self.self_shame, "admiration": self.admiration,
            "reproach": self.reproach, "gratitude": self.gratitude, "anger": self.anger,
            "love": self.love, "hate": self.hate, "distress": self.distress,
            "sadness": self.sadness, "happiness": self.happiness
        }
    
    def get_dominant(self) -> str:
        """获取主导情绪"""
        emotions = self.to_dict()
        if not emotions:
            return "neutral"
        return max(emotions, key=emotions.get)
    
    def get_intensity(self) -> float:
        """获取整体情绪强度"""
        emotions = self.to_dict()
        if not emotions:
            return 0.0
        return sum(emotions.values()) / len(emotions)


class OCCEngine:
    """
    OCC 情绪引擎
    
    根据认知评估产生情绪反应
    """
    
    def __init__(self):
        self.state = OCCState()
        self.history: List[OCCState] = []
    
    def appraise(self, event: Dict[str, Any], context: Dict[str, Any] = None) -> OCCState:
        """
        评估事件，产生情绪
        
        Args:
            event: 事件描述
                - type: "event" | "action" | "object"
                - desirability: 期望程度
                - goal_relevant: 是否与目标相关
                - ...其他评估维度
            context: 上下文
        
        Returns:
            更新后的情绪状态
        """
        context = context or {}
        appraisal = self._create_appraisal(event)
        
        # 根据评估结果计算情绪
        self._compute_emotions(appraisal)
        
        # 记录历史
        self.history.append(OCCState(
            hope=self.state.hope,
            joy=self.state.joy,
            satisfaction=self.state.satisfaction,
            relief=self.state.relief,
            disappointment=self.state.disappointment,
            fear=self.state.fear,
            pride=self.state.pride,
            shame=self.state.shame,
            self_pride=self.state.self_pride,
            self_shame=self.state.self_shame,
            admiration=self.state.admiration,
            reproach=self.state.reproach,
            gratitude=self.state.gratitude,
            anger=self.state.anger,
            love=self.state.love,
            hate=self.state.hate,
            distress=self.state.distress,
            sadness=self.state.sadness,
            happiness=self.state.happiness
        ))
        
        return self.state
    
    def _create_appraisal(self, event: Dict[str, Any]) -> Appraisal:
        """根据事件创建评估"""
        appraisal = Appraisal()
        
        event_type = event.get("type", "event")
        
        if event_type == "event":
            # 事件评估
            appraisal.desirability = event.get("desirability", 0.0)
            appraisal.likelihood = event.get("likelihood", 0.5)
            appraisal.expectedness = event.get("expectedness", 0.5)
            appraisal.goal_relevant = event.get("goal_relevant", True)
            appraisal.realized = event.get("realized", True)
            
        elif event_type == "action":
            # 行为评估
            appraisal.praiseworthiness = event.get("praiseworthiness", 0.0)
            appraisal.causal_attribution_self = event.get("causal_attribution_self", 0.0)
            appraisal.causal_attribution_other = event.get("causal_attribution_other", 0.0)
            
        elif event_type == "object":
            # 对象评估
            appraisal.attractiveness = event.get("attractiveness", 0.0)
        
        return appraisal
    
    def _compute_emotions(self, appraisal: Appraisal):
        """根据评估结果计算各情绪强度"""
        
        # 事件结果情绪
        if appraisal.realized:
            if appraisal.desirability > 0:
                # 正面结果
                if appraisal.likelihood > 0.5:
                    self.state.hope = appraisal.desirability * appraisal.likelihood
                    self.state.joy = appraisal.desirability
                else:
                    self.state.relief = appraisal.desirability * (1 - appraisal.likelihood)
                self.state.satisfaction = appraisal.desirability * 0.8
            else:
                # 负面结果
                if appraisal.likelihood > 0.5:
                    self.state.fear = abs(appraisal.desirability) * appraisal.likelihood
                self.state.disappointment = abs(appraisal.desirability) * 0.8
                self.state.sadness = abs(appraisal.desirability) * 0.5
        
        # 行为情绪
        if appraisal.praiseworthiness != 0:
            if appraisal.causal_attribution_self > 0:
                self.state.self_pride = appraisal.praiseworthiness * appraisal.causal_attribution_self
            elif appraisal.causal_attribution_self < 0:
                self.state.self_shame = abs(appraisal.praiseworthiness) * abs(appraisal.causal_attribution_self)
            
            if appraisal.causal_attribution_other > 0:
                self.state.admiration = appraisal.praiseworthiness * appraisal.causal_attribution_other
            elif appraisal.causal_attribution_other < 0:
                self.state.reproach = abs(appraisal.praiseworthiness) * abs(appraisal.causal_attribution_other)
        
        # 对象情绪
        if appraisal.attractiveness > 0:
            self.state.love = appraisal.attractiveness
        elif appraisal.attractiveness < 0:
            self.state.hate = abs(appraisal.attractiveness)
        
        # 复合情绪
        self.state.happiness = (self.state.joy + self.state.satisfaction) / 2
        self.state.distress = (self.state.sadness + self.state.fear) / 2
        
        # 限制范围 [0, 1]
        for key in self.state.__dict__:
            setattr(self.state, key, min(1.0, max(0.0, getattr(self.state, key))))
    
    def decay(self, time_delta: float, half_life: float = 3600):
        """
        情绪衰减
        
        Args:
            time_delta: 经过时间(秒)
            half_life: 半衰期(秒)
        """
        decay_factor = math.exp(-math.log(2) * time_delta / half_life)
        
        for key in self.state.__dict__:
            current = getattr(self.state, key)
            setattr(self.state, key, current * decay_factor)
    
    def reset(self):
        """重置情绪"""
        for key in self.state.__dict__:
            setattr(self.state, key, 0.0)
        self.history.clear()
    
    def decay_differential(self, time_delta: float, config: "OCCHalfLifeConfig" = None):
        """差异化衰减 - 不同情绪有不同的半衰期

        joy 消退慢（好心情持续久），anger 消退快（气过了就好了）

        Args:
            time_delta: 经过的时间（秒）
            config: 半衰期配置
        """
        import math
        config = config or OCCHalfLifeConfig()

        emotions = self.state.to_dict()
        for emotion_name, current in emotions.items():
            if current <= 0.001:  # 忽略极小值
                continue
            half_life = config.get(emotion_name)
            decay_factor = math.exp(-math.log(2) * time_delta / half_life)
            setattr(self.state, emotion_name, current * decay_factor)


@dataclass
class OCCHalfLifeConfig:
    """OCC 情绪的差异化半衰期配置

    不同情绪有不同的衰减速度，模拟真实的人类情绪特点：
    - 愤怒消退快（15分钟）
    - 惊讶很短暂（10分钟）
    - 爱持续久（24小时）
    """

    # 快速衰减（秒）
    anger: float = 900           # 愤怒来得快去得快
    surprise: float = 600        # 惊讶很短暂
    fear: float = 1200           # 恐惧消退较快
    fear_confounding: float = 1200

    # 中等衰减
    joy: float = 3600            # 喜悦持续约 1 小时
    sadness: float = 5400        # 悲伤持续较久
    disappointment: float = 3600 # 失望中等持续
    distress: float = 2700       # 苦恼中等
    relief: float = 1800         # 宽慰较快

    # 慢速衰减
    love: float = 86400          # 爱是长久的
    hate: float = 43200          # 恨也持续很久
    pride: float = 7200          # 自豪感持续较久
    shame: float = 14400         # 羞耻感更持久
    self_pride: float = 5400    # 自我自豪较久
    self_shame: float = 10800    # 自我羞耻更久

    # 行为评估情绪
    hope: float = 3600           # 希望中等
    satisfaction: float = 2700   # 满意中等
    admiration: float = 3600     # 钦佩中等
    reproach: float = 3600        # 责备中等
    gratitude: float = 7200      # 感激持续

    # 默认
    default: float = 3600

    def get(self, emotion_name: str) -> float:
        """获取指定情绪的半衰期"""
        return getattr(self, emotion_name, self.default)


class OCCToPADProjector:
    """
    OCC 情绪 → PAD 维度投影

    [职责] 将离散情绪映射到连续维度空间
    [依据] Mehrabian (1996) 情绪-PAD 映射 + OCC 模型语义
    [可替换性] 映射矩阵可配置化
    """

    # 映射矩阵: emotion_name → (pleasure, arousal, dominance) 权重
    PROJECTION_MATRIX = {
        # 正面事件情绪
        "joy":            (0.8,  0.3,  0.2),
        "hope":           (0.5,  0.2,  0.1),
        "satisfaction":   (0.6,  -0.1, 0.3),
        "relief":         (0.4,  -0.3, 0.2),
        "happiness":      (0.7,  0.2,  0.2),

        # 负面事件情绪
        "fear":           (-0.6, 0.7, -0.6),
        "disappointment": (-0.5, -0.2, -0.3),
        "sadness":        (-0.7, -0.3, -0.4),
        "distress":       (-0.6, 0.4, -0.5),

        # 行为评估情绪
        "pride":          (0.5,  0.3,  0.6),
        "shame":          (-0.5, 0.2, -0.6),
        "self_pride":     (0.4,  0.2,  0.5),
        "self_shame":     (-0.4, 0.3, -0.5),
        "admiration":     (0.5,  0.2, -0.1),
        "reproach":       (-0.4, 0.3,  0.3),

        # 复合情绪
        "gratitude":      (0.6,  0.1, -0.1),
        "anger":          (-0.5, 0.7,  0.5),

        # 对象情绪
        "love":           (0.7,  0.3,  0.1),
        "hate":           (-0.6, 0.5,  0.3),
    }

    @classmethod
    def project(cls, occ_state: OCCState) -> Dict[str, float]:
        """将 OCC 情绪状态投影到 PAD 空间

        Args:
            occ_state: OCC 情绪状态

        Returns:
            PAD 向量 dict: {pleasure, arousal, dominance}
        """
        p, a, d = 0.0, 0.0, 0.0
        emotions = occ_state.to_dict()

        # 加权求和
        for emotion_name, intensity in emotions.items():
            if intensity <= 0.0:
                continue
            weights = cls.PROJECTION_MATRIX.get(emotion_name, (0, 0, 0))
            p += intensity * weights[0]
            a += intensity * weights[1]
            d += intensity * weights[2]

        # 归一化到 [-1, 1]
        return {
            "pleasure": max(-1.0, min(1.0, p)),
            "arousal":  max(-1.0, min(1.0, a)),
            "dominance": max(-1.0, min(1.0, d)),
        }

    @classmethod
    def project_neurotransmitters(cls, occ_state: OCCState) -> Dict[str, float]:
        """从 OCC 情绪推导神经递质水平

        Args:
            occ_state: OCC 情绪状态

        Returns:
            神经递质 dict: {dopamine, cortisol}
        """
        emotions = occ_state.to_dict()

        # 多巴胺：积极情绪驱动
        dopamine = 0.5  # 基线
        dopamine += emotions.get("joy", 0) * 0.3
        dopamine += emotions.get("satisfaction", 0) * 0.2
        dopamine += emotions.get("hope", 0) * 0.2
        dopamine += emotions.get("love", 0) * 0.15
        dopamine += emotions.get("pride", 0) * 0.15
        dopamine += emotions.get("admiration", 0) * 0.1
        dopamine += emotions.get("gratitude", 0) * 0.15
        dopamine -= emotions.get("sadness", 0) * 0.2
        dopamine -= emotions.get("disappointment", 0) * 0.15
        dopamine -= emotions.get("shame", 0) * 0.1

        # 皮质醇：压力/威胁情绪驱动
        cortisol = 0.3  # 基线
        cortisol += emotions.get("fear", 0) * 0.3
        cortisol += emotions.get("anger", 0) * 0.25
        cortisol += emotions.get("distress", 0) * 0.2
        cortisol += emotions.get("shame", 0) * 0.15
        cortisol += emotions.get("self_shame", 0) * 0.15
        cortisol += emotions.get("reproach", 0) * 0.1
        cortisol -= emotions.get("relief", 0) * 0.15
        cortisol -= emotions.get("joy", 0) * 0.1
        cortisol -= emotions.get("satisfaction", 0) * 0.1

        return {
            "dopamine": max(0.0, min(1.0, dopamine)),
            "cortisol": max(0.0, min(1.0, cortisol)),
        }


# 便捷函数
def create_occ_engine() -> OCCEngine:
    """创建 OCC 引擎"""
    return OCCEngine()
