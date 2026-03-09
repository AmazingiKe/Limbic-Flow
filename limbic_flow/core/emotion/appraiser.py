"""
LLM 驱动的认知评估器

[职责] 用 LLM 理解用户输入的语义，产出 OCC Appraisal
[设计] 将「情绪理解」从关键词匹配升级为语义理解
[可替换性] 可替换为本地模型、规则引擎，或外部 NLU 服务
"""

import json
import re
from typing import Dict, Any, Optional


class LLMAppraiser:
    """
    LLM 驱动的认知评估器

    使用 LLM 对用户输入进行深层次的语义理解，
    生成 OCC 模型所需的认知评估结果。
    """

    APPRAISAL_PROMPT = """你是一个情绪认知评估器。分析用户的输入，返回以下 JSON：

{
  "event_type": "event" | "action" | "object",
  "desirability": -1.0 ~ 1.0,
  "desirability_for_other": -1.0 ~ 1.0,
  "praiseworthiness": -1.0 ~ 1.0,
  "attractiveness": -1.0 ~ 1.0,
  "likelihood": 0.0 ~ 1.0,
  "expectedness": 0.0 ~ 1.0,
  "causal_attribution_self": -1.0 ~ 1.0,
  "causal_attribution_other": -1.0 ~ 1.0,
  "realized": true | false,
  "goal_relevant": true | false
}

只返回 JSON，不要解释。"""

    def __init__(self, llm=None):
        """初始化评估器

        Args:
            llm: LLM 实例（来自 LLMFactory），可选
        """
        self.llm = llm

    def appraise(self, user_input: str, context: Dict = None):
        """用 LLM 对用户输入进行认知评估

        Args:
            user_input: 用户输入文本
            context: 额外上下文

        Returns:
            Appraisal: 认知评估结果
        """
        from limbic_flow.core.emotion.occ import Appraisal
        
        context = context or {}

        # 如果有 LLM，尝试使用
        if self.llm:
            try:
                response = self.llm.chat_simple(
                    prompt=f"用户说: {user_input}",
                    system_prompt=self.APPRAISAL_PROMPT,
                    temperature=0.3
                )
                data = json.loads(response.content)
                return self._parse_appraisal(data)
            except (json.JSONDecodeError, AttributeError, Exception):
                pass

        # 回退到规则引擎
        return self._rule_based_appraise(user_input)

    def _parse_appraisal(self, data: Dict) -> "Appraisal":
        """解析 LLM 返回的评估 JSON"""
        from limbic_flow.core.emotion.occ import Appraisal
        
        return Appraisal(
            desirability=self._clamp(data.get("desirability", 0.0)),
            desirability_for_other=self._clamp(data.get("desirability_for_other", 0.0)),
            praiseworthiness=self._clamp(data.get("praiseworthiness", 0.0)),
            attractiveness=self._clamp(data.get("attractiveness", 0.0)),
            likelihood=max(0.0, min(1.0, data.get("likelihood", 0.5))),
            expectedness=max(0.0, min(1.0, data.get("expectedness", 0.5))),
            causal_attribution_self=self._clamp(data.get("causal_attribution_self", 0.0)),
            causal_attribution_other=self._clamp(data.get("causal_attribution_other", 0.0)),
            realized=data.get("realized", True),
            goal_relevant=data.get("goal_relevant", True),
        )

    def _rule_based_appraise(self, user_input: str):
        """规则引擎回退

        当 LLM 不可用时，使用简化的规则引擎进行评估。
        """
        from limbic_flow.core.emotion.occ import Appraisal
        
        text = user_input.lower()
        appraisal = Appraisal()

        # 期望程度判断
        if any(w in text for w in ["开心", "happy", "好事", "成功", "太好了", "好开心", "棒", "喜欢", "高兴", "开心"]):
            appraisal.desirability = 0.7
            appraisal.realized = True
        elif any(w in text for w in ["伤心", "sad", "失败", "难过", "糟糕", "讨厌", "不喜欢", "悲伤"]):
            appraisal.desirability = -0.7
            appraisal.realized = True
        elif any(w in text for w in ["害怕", "fear", "担心", "紧张", "焦虑", "恐惧"]):
            appraisal.desirability = -0.5
            appraisal.likelihood = 0.7
            appraisal.realized = False
        elif any(w in text for w in ["希望", "hope", "期待", "希望能", "想"]):
            appraisal.desirability = 0.5
            appraisal.likelihood = 0.6
            appraisal.realized = False
        elif any(w in text for w in ["生气", "angry", "愤怒", "火大", "不爽", "气"]):
            appraisal.desirability = -0.6
            appraisal.praiseworthiness = -0.5
            appraisal.causal_attribution_other = 0.8
            appraisal.realized = True
        elif any(w in text for w in ["骄傲", "proud", "自豪", "厉害", "棒"]):
            appraisal.praiseworthiness = 0.7
            appraisal.causal_attribution_self = 0.8
            appraisal.realized = True
        elif any(w in text for w in ["谢谢", "感谢", "感激"]):
            appraisal.desirability = 0.5
            appraisal.praiseworthiness = 0.6
            appraisal.realized = True

        # 归因推断
        if any(w in text for w in ["都怪他", "是他", "她害的", "他让我"]):
            appraisal.causal_attribution_other = 0.7
        elif any(w in text for w in ["都怪我", "是我不好", "我的错"]):
            appraisal.causal_attribution_self = 0.7

        return appraisal

    @staticmethod
    def _clamp(v: float) -> float:
        """限制值在 [-1, 1] 范围内"""
        return max(-1.0, min(1.0, v))


def create_appraiser(llm=None) -> LLMAppraiser:
    """创建 LLM 评估器"""
    return LLMAppraiser(llm)
