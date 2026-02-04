from typing import Dict, Any, Optional
from limbic_flow.core.types import CognitiveState
from limbic_flow.core.ai.factory import LLMFactory
from limbic_flow.core.location import LocationDetector
from limbic_flow.core.brain.persona import PersonaManager

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
        self.persona_manager = PersonaManager()

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
            state.final_response_text = response.content
            state.content = response.content
        except Exception as e:
            # 回退机制
            print(f"LLM Error: {e}")
            state.final_response_text = self._fallback_expression(state)
            state.content = state.final_response_text

        return state

    def _build_system_prompt(self, state: CognitiveState) -> str:
        location_summary = self.location_detector.get_location_summary(self.user_location)
        return self.persona_manager.render_system_prompt(state, location_summary)

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
        if state.pad_vector['pleasure'] > 0.3:
            return "我现在感觉很开心！有什么我可以帮忙的吗？"
        elif state.pad_vector['pleasure'] < -0.3:
            return "我现在有点沮丧。你有什么想聊的吗？"
        elif state.pad_vector['arousal'] > 0.3:
            return "我现在感觉精力充沛！你在想什么？"
        elif state.neurotransmitters['cortisol'] > 0.7:
            return "我现在感觉压力很大。让我们冷静一下。"
        else:
            return "我在这里。你想讨论什么？"
