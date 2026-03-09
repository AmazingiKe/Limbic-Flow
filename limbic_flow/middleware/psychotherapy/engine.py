"""
心理治疗引擎 - 基于研究文档实现

参考:
- PSYCHOTHERAPY_AI_MODELS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum
import random


class TherapyType(Enum):
    """治疗类型"""
    CBT = "cbt"          # 认知行为疗法
    DBT = "dbt"          # 辩证行为疗法
    ACT = "act"          # 接纳与承诺疗法
    TRAUMA = "trauma"    # 创伤恢复


@dataclass
class TherapeuticIntervention:
    """治疗干预"""
    type: TherapyType
    technique: str
    description: str
    prompt: str
    effectiveness: float = 0.5


class CBTTherapy:
    """
    认知行为疗法 (CBT)
    
    研究参考:
    - 认知扭曲识别
    - 苏格拉底提问
    - 信念更新
    """
    
    def __init__(self):
        self.cognitive_distortions = {
            "全或无": ["总是", "从不", "完全", "绝对"],
            "过度概括": ["所有", "每个", "永远"],
            "心理过滤": ["只", "仅仅", "只有"],
            "否定正面": ["但是", "不过"],
            "妄下结论": ["他会", "她会", "他们会"],
            "灾难化": ["可怕", "灾难", "糟糕"],
            "情绪推理": ["我觉得", "我感到"],
            "应该陈述": ["应该", "必须", "需要"],
            "个人化": ["都是因为", "责任在于"],
        }
    
    def identify_distortions(self, thought: str) -> List[Dict]:
        """
        识别认知扭曲
        
        Args:
            thought: 来访者的想法
        
        Returns:
            List[Dict]: 识别出的扭曲
        """
        distortions = []
        thought_lower = thought.lower()
        
        for distortion_type, keywords in self.cognitive_distortions.items():
            matches = [kw for kw in keywords if kw in thought_lower]
            if matches:
                distortions.append({
                    "type": distortion_type,
                    "matches": matches,
                    "confidence": len(matches) / len(keywords)
                })
        
        return distortions
    
    def socratic_questioning(self, distortion: Dict, thought: str) -> List[str]:
        """
        苏格拉底提问
        
        帮助来访者自己发现答案
        """
        questions = []
        
        q_map = {
            "全或无": [
                "有没有例外情况?",
                "如果用百分比来评估,真的是100%吗?"
            ],
            "过度概括": [
                "这个例子能代表所有情况吗?",
                "过去有这样的例子吗?"
            ],
            "灾难化": [
                "最坏的结果是什么?最可能的结果呢?",
                "如果朋友遇到同样的事,你会怎么说?"
            ],
            "情绪推理": [
                "情绪能代表事实吗?",
                "有什么证据支持你的感受?"
            ],
            "应该陈述": [
                "为什么你觉得应该?",
                "这是谁的规则?"
            ],
        }
        
        q_map.get(distortion["type"], [
            "你能详细说说吗?",
            "是什么让你这么觉得?",
        ])
        
        return questions
    
    def generate_challenge(self, thought: str, distortion: Dict) -> str:
        """
        生成挑战性问题
        
        帮助来访者重新审视想法
        """
        challenges = {
            "全或无": "把事情想成'全或无'是否忽略了中间状态?",
            "过度概括": "一个例子能否代表全部?",
            "心理过滤": "是否只关注了负面而忽略了正面?",
            "否定正面": "那些正面因素是否被忽视了?",
            "灾难化": "即使最坏情况发生,真的那么可怕吗?",
            "情绪推理": "你的感受≠事实,有什么证据?",
        }
        
        return challenges.get(
            distortion["type"], 
            "让我们换个角度看看这个问题"
        )


class DBTTherapy:
    """
    辩证行为疗法 (DBT)
    
    研究参考:
    - 正念
    - 痛苦耐受
    - 情绪调节
    - 人际效能
    """
    
    def __init__(self):
        self.skills = {
            "mindfulness": {
                "是什么": "专注当下,不评判地觉察",
                "技术": ["观呼吸", "身体扫描", "五感觉察"]
            },
            "distress_tolerance": {
                "是什么": "在痛苦中生存而不行动",
                "技术": ["TIP", "自我安抚", "接纳"]
            },
            "emotion_regulation": {
                "是什么": "改变情绪反应",
                "技术": ["反流", "情绪释放", "行为激活"]
            },
            "interpersonal": {
                "是什么": "有效人际沟通",
                "技术": ["DEAR MAN", "快速请求", "说 不"]
            }
        }
    
    def get_skill(self, category: str, situation: Dict) -> TherapeuticIntervention:
        """获取技能建议"""
        
        if category == "mindfulness":
            return self._mindfulness_intervention(situation)
        elif category == "distress_tolerance":
            return self._distress_tolerance_intervention(situation)
        elif category == "emotion_regulation":
            return self._emotion_regulation_intervention(situation)
        else:
            return self._interpersonal_intervention(situation)
    
    def _mindfulness_intervention(self, situation: Dict) -> TherapeuticIntervention:
        """正念干预"""
        techniques = ["观呼吸", "4-7-8呼吸", "身体扫描", "五感觉察"]
        
        return TherapeuticIntervention(
            type=TherapyType.DBT,
            technique="mindfulness",
            description="通过正念回到当下",
            prompt=f"现在,让我们做几次深呼吸。聚焦于你的{techniques[random.randint(0, len(techniques)-1)]}。不需要评判,只是觉察。"
        )
    
    def _distress_tolerance_intervention(self, situation: Dict) -> TherapeuticIntervention:
        """痛苦耐受干预"""
        intensity = situation.get("intensity", 0.5)
        
        if intensity > 0.7:
            # 高强度: 使用TIP技术
            prompt = "现在情况很强烈。让我们用TIP技术: 冷敷(把冰块放在额头上)、剧烈运动(做几次上下楼梯)、放松(收紧然后放松肌肉)、腹式呼吸。"
        else:
            # 中低强度: 自我安抚
            prompt = "尝试用5-4-3-2-1技术: 看到5样东西、听到4样、摸到3样、闻2样、尝1样。"
        
        return TherapeuticIntervention(
            type=TherapyType.DBT,
            technique="distress_tolerance",
            description="在痛苦中保持平衡",
            prompt=prompt
        )
    
    def _emotion_regulation_intervention(self, situation: Dict) -> TherapeuticIntervention:
        """情绪调节干预"""
        emotion = situation.get("emotion", "")
        
        prompt = f"你的{emotion}情绪是有效的信号。现在让我们: 1) 给这个情绪命名 2) 确认它 3) 允许它存在。"
        
        return TherapeuticIntervention(
            type=TherapyType.DBT,
            technique="emotion_regulation",
            description="理解并调节情绪",
            prompt=prompt
        )
    
    def _interpersonal_intervention(self, situation: Dict) -> TherapeuticIntervention:
        """人际效能干预"""
        
        prompt = "在这种情况下,记住DEAR MAN: D-描述情况, E-表达你的感受, A-主张你的需求, R-强化(说明为什么), M-保持专注, A-合作, N-谈判。"
        
        return TherapeuticIntervention(
            type=TherapyType.DBT,
            technique="interpersonal",
            description="有效表达需求",
            prompt=prompt
        )


class ACTTherapy:
    """
    接纳与承诺疗法 (ACT)
    
    研究参考:
    - 心理灵活性六边形
    - 接纳
    - 认知解离
    - 当下觉察
    - 自我如背景
    - 价值澄清
    - 承诺行动
    """
    
    def __init__(self):
        self.hexaflex = {
            "接纳": "接受内部体验",
            "认知解离": "与想法保持距离",
            "当下觉察": "专注当前时刻",
            "自我如背景": "观察性自我",
            "价值澄清": "明确什么是重要的",
            "承诺行动": "按价值行动"
        }
    
    def get_intervention(self, target: str, context: Dict) -> TherapeuticIntervention:
        """获取ACT干预"""
        
        interventions = {
            "接纳": self._acceptance,
            "认知解离": self._defusion,
            "当下觉察": self._present_moment,
            "自我如背景": self._self_as_context,
            "价值澄清": self._values,
            "承诺行动": self._committed_action
        }
        
        return interventions.get(target, self._acceptance)(context)
    
    def _acceptance(self, context: Dict) -> TherapeuticIntervention:
        """接纳干预"""
        
        prompt = "让你的想法和情绪如其所是。不需要赶走它们,不需要改变它们。只是承认:'此刻,我正在体验...'"
        
        return TherapeuticIntervention(
            type=TherapyType.ACT,
            technique="acceptance",
            description="接纳当前体验",
            prompt=prompt
        )
    
    def _defusion(self, context: Dict) -> TherapeuticIntervention:
        """认知解离"""
        
        prompt = "把你的想法当作路过的云朵,你只是看着它们飘过。可以试着在想法前加上'我有一个想法...'来创造距离。"
        
        return TherapeuticIntervention(
            type=TherapyType.ACT,
            technique="defusion",
            description="与想法保持距离",
            prompt=prompt
        )
    
    def _present_moment(self, context: Dict) -> TherapeuticIntervention:
        """当下觉察"""
        
        prompt = "现在,完全回到这个时刻。注意你此刻听到的、看到的、感觉到的。不需要思考过去或未来。"
        
        return TherapeuticIntervention(
            type=TherapyType.ACT,
            technique="present_moment",
            description="专注当下",
            prompt=prompt
        )
    
    def _self_as_context(self, context: Dict) -> TherapeuticIntervention:
        """自我如背景"""
        
        prompt = "你是那个觉察这些想法和感受的'观察者'。这个观察者的你是稳定的、持续的背景。"
        
        return TherapeuticIntervention(
            type=TherapyType.ACT,
            technique="self_as_context",
            description="观察性自我",
            prompt=prompt
        )
    
    def _values(self, context: Dict) -> TherapeuticIntervention:
        """价值澄清"""
        
        prompt = "如果没有任何限制,你真正想过什么样的生活?什么对你来说是真正重要的?"
        
        return TherapeuticIntervention(
            type=TherapyType.ACT,
            technique="values",
            description="明确个人价值",
            prompt=prompt
        )
    
    def _committed_action(self, context: Dict) -> TherapeuticIntervention:
        """承诺行动"""
        
        prompt = "基于你重视的东西,今天你能做一件小事来靠近你想要的生活吗?"
        
        return TherapeuticIntervention(
            type=TherapyType.ACT,
            technique="committed_action",
            description="按价值行动",
            prompt=prompt
        )


class PsychotherapyEngine:
    """
    心理治疗引擎
    
    整合多种治疗方法,根据情况选择合适干预
    """
    
    def __init__(self):
        self.cbt = CBTTherapy()
        self.dbt = DBTTherapy()
        self.act = ACTTherapy()
        
        # 选择规则
        self.selection_rules = {
            "cognitive_distortions": TherapyType.CBT,
            "emotional_dysregulation": TherapyType.DBT,
            "avoidance": TherapyType.ACT,
            "trauma": TherapyType.TRAUMA,
            "default": TherapyType.CBT
        }
    
    def analyze_and_intervene(
        self,
        user_input: str,
        emotion_state: Dict,
        context: Dict
    ) -> TherapeuticIntervention:
        """
        分析并提供干预
        
        Args:
            user_input: 用户输入
            emotion_state: 情绪状态
            context: 上下文
        
        Returns:
            TherapeuticIntervention: 治疗干预
        """
        # 检测问题类型
        issue_type = self._detect_issue_type(user_input, emotion_state)
        
        # 选择治疗类型
        therapy_type = self.selection_rules.get(issue_type, TherapyType.CBT)
        
        # 生成干预
        if therapy_type == TherapyType.CBT:
            return self._cbt_intervention(user_input, emotion_state)
        elif therapy_type == TherapyType.DBT:
            return self._dbt_intervention(emotion_state)
        elif therapy_type == TherapyType.ACT:
            return self._act_intervention(context)
        else:
            return self._cbt_intervention(user_input, emotion_state)
    
    def _detect_issue_type(self, user_input: str, emotion_state: Dict) -> str:
        """检测问题类型"""
        
        # 检查认知扭曲
        distortions = self.cbt.identify_distortions(user_input)
        if distortions:
            return "cognitive_distortions"
        
        # 检查情绪失调
        arousal = emotion_state.get("arousal", 0)
        if arousal > 0.7:
            return "emotional_dysregulation"
        
        # 检查回避
        avoidance_words = ["不想", "不敢", "害怕", "回避"]
        if any(w in user_input for w in avoidance_words):
            return "avoidance"
        
        # 检查创伤相关
        trauma_words = ["创伤", "害怕", "闪回", "惊恐"]
        if any(w in user_input for w in trauma_words):
            return "trauma"
        
        return "default"
    
    def _cbt_intervention(self, user_input: str, emotion_state: Dict) -> TherapeuticIntervention:
        """CBT干预"""
        
        distortions = self.cbt.identify_distortions(user_input)
        
        if distortions:
            # 有认知扭曲,进行挑战
            challenge = self.cbt.generate_challenge(user_input, distortions[0])
            
            return TherapeuticIntervention(
                type=TherapyType.CBT,
                technique="cognitive_challenge",
                description="挑战认知扭曲",
                prompt=challenge
            )
        else:
            # 无扭曲,使用苏格拉底提问
            return TherapeuticIntervention(
                type=TherapyType.CBT,
                technique="exploration",
                description="探索想法",
                prompt="能多说说是什么让你这么想的吗?"
            )
    
    def _dbt_intervention(self, emotion_state: Dict) -> TherapeuticIntervention:
        """DBT干预"""
        
        intensity = emotion_state.get("arousal", 0.5)
        
        return self.dbt.get_skill("distress_tolerance", {
            "intensity": intensity,
            "emotion": emotion_state.get("emotion", "")
        })
    
    def _act_intervention(self, context: Dict) -> TherapeuticIntervention:
        """ACT干预"""
        
        targets = list(self.act.hexaflex.keys())
        target = random.choice(targets)
        
        return self.act.get_intervention(target, context)


# 示例
if __name__ == "__main__":
    engine = PsychotherapyEngine()
    
    # 测试CBT
    intervention = engine.analyze_and_intervene(
        "我总是做不好,完全是个失败者",
        {"arousal": 0.6, "pleasure": -0.3},
        {}
    )
    
    print(f"Type: {intervention.type.value}")
    print(f"Technique: {intervention.technique}")
    print(f"Prompt: {intervention.prompt}")
