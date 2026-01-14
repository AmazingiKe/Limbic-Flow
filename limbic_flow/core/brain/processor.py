from typing import Dict, Any, Optional
from limbic_flow.core.types import CognitiveState
from limbic_flow.core.ai.factory import LLMFactory
from limbic_flow.core.location import LocationDetector

class Brain:
    """
    [职责] 大脑/新皮层 - 负责高级认知、内省与文本生成
    [场景] 接收扭曲后的记忆，生成最终回复内容
    [可替换性] 可替换为不同的大模型或认知架构
    """
    
    def __init__(self, llm_provider: Optional[str] = None):
        self.llm_factory = LLMFactory()
        self.llm = self.llm_factory.create_llm(llm_provider)
        self.location_detector = LocationDetector()
        self.user_location = self.location_detector.detect_location()

    def process(self, state: CognitiveState) -> CognitiveState:
        """
        [职责] 处理认知状态，生成回复
        [场景] Pipeline 调度调用
        """
        # 1. 构建提示词
        system_prompt = self._build_system_prompt(state)
        user_prompt = self._build_user_prompt(state)
        
        # 2. 调用 LLM 生成内容
        try:
            # TODO: 支持流式思考 (Introspection)
            response = self.llm.chat_simple(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.8
            )
            state.content = response.content
        except Exception as e:
            # 回退机制
            print(f"LLM Error: {e}")
            state.content = self._fallback_expression(state)
            
        return state

    def _build_system_prompt(self, state: CognitiveState) -> str:
        # 从 State 中提取情绪
        pleasure = state.pleasure
        arousal = state.arousal
        dominance = state.dominance
        cortisol = state.cortisol
        
        # 生成情绪表达风格指南
        emotion_style_guide = ""
        
        if pleasure > 0.5:
            emotion_style_guide += "使用非常积极、热情的语气，充满活力。可以使用更多的感叹号和积极的表情符号。\n"
        elif pleasure > 0.2:
            emotion_style_guide += "使用友好、温暖的语气，带有轻微的积极情绪。可以适当使用表情符号。\n"
        elif pleasure < -0.5:
            emotion_style_guide += "使用温和、理解的语气，带有轻微的忧郁。避免使用过多的感叹号和过于活泼的表达。\n"
        elif pleasure < -0.2:
            emotion_style_guide += "使用平静、稳重的语气，保持中性偏温和。\n"
        else:
            emotion_style_guide += "使用平静、自然的语气，保持中性。\n"
        
        if arousal > 0.5:
            emotion_style_guide += "回应应该更加生动、有活力，可能会稍微长一些，表达更丰富的细节。\n"
        elif arousal < -0.5:
            emotion_style_guide += "回应应该简洁、平静，节奏较慢，避免过于复杂的表达。\n"
        
        if cortisol > 0.7:
            emotion_style_guide += "表现出轻微的紧张或专注，回应会更加直接和有条理。\n"
        
        location_summary = self.location_detector.get_location_summary(self.user_location)
        
        # 提取用户信息 (假设在 Context 中)
        user_info_str = ""
        user_info = state.context.get("user_info", {})
        if user_info:
            user_info_str = "用户信息：\n"
            if "name" in user_info:
                user_info_str += f"- 名字: {user_info['name']}\n"
            user_info_str += "\n"
        
        return f"""你是一个具有人类情绪特征的 AI 助手。

表达风格指南：
{emotion_style_guide}

{user_info_str}
用户的位置信息：
{location_summary}

请根据上述风格指南、用户信息和用户的位置信息，以自然、真实的方式回应。
注意：
1. 保持友好、温暖的语气，避免冷漠的回应
2. 绝对不要直接陈述你的情绪状态或情绪数值，而是通过语言风格和语气来体现
3. 如果你已经知道用户的名字，请在回应中使用他们的名字
4. 回应应该直接回答用户的问题，不要重复无关的内容
"""

    def _build_user_prompt(self, state: CognitiveState) -> str:
        memories = state.distorted_memories # 使用扭曲后的记忆
        
        prompt = "用户刚刚说：\n"
        prompt += state.user_input + "\n\n"
        
        user_info = state.context.get("user_info", {})
        if user_info:
            prompt += "用户信息：\n"
            if "name" in user_info:
                prompt += f"- 名字: {user_info['name']}\n"
            prompt += "\n"
        
        if memories:
            prompt += "相关的记忆（可能被你的情绪扭曲）：\n"
            for i, memory in enumerate(memories, 1):
                if isinstance(memory, dict):
                    if "user_input" in memory:
                        prompt += f"{i}. 用户说: '{memory['user_input'][:100]}...'\n"
                    if "system_response" in memory:
                        prompt += f"   系统回应: '{memory['system_response'][:100]}...'\n"
                else:
                    prompt += f"{i}. {memory}\n"
            prompt += "\n"
        
        prompt += "请根据用户的输入和用户信息，给出一个自然、真实的回应。\n"
        return prompt

    def _fallback_expression(self, state: CognitiveState) -> str:
        if state.pleasure > 0.3:
            return "我现在感觉很开心！有什么我可以帮忙的吗？"
        elif state.pleasure < -0.3:
            return "我现在有点沮丧。你有什么想聊的吗？"
        elif state.arousal > 0.3:
            return "我现在感觉精力充沛！你在想什么？"
        elif state.cortisol > 0.7:
            return "我现在感觉压力很大。让我们冷静一下。"
        else:
            return "我在这里。你想讨论什么？"
