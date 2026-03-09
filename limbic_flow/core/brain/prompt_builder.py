"""
提示词构建器 - 为大脑生成提示词

[职责] 将情绪状态、记忆、上下文转换为 LLM 可理解的提示词
[设计] 纯函数式，便于测试
"""

from typing import Dict, Any, List, Optional
from limbic_flow.core.types import CognitiveState


class PromptBuilder:
    """
    提示词构建器
    
    [比喻] 就像一个"翻译官"，把情绪状态"翻译"成prompt
    """
    
    def __init__(self):
        pass
    
    def build_system_prompt(
        self, 
        state: CognitiveState,
        location_summary: str = ""
    ) -> str:
        """
        构建系统提示词 (支持 OCC 风格)
        
        Args:
            state: 认知状态
            location_summary: 位置摘要
        
        Returns:
            系统提示词
        """
        # 用户信息
        user_info_str = self._build_user_info(state.context.get("user_info", {}))
        
        # 主导情绪信息（如果存在）
        emotion_info = ""
        if hasattr(state, 'dominant_emotion') and state.dominant_emotion:
            intensity = getattr(state, 'emotion_intensity', 0.5)
            emotion_info = f"\n当前情绪: {state.dominant_emotion} (强度: {intensity:.1f})"
            
            # 如果有 OCC 状态，生成 OCC 风格指南
            if hasattr(state, 'occ_state') and state.occ_state:
                style_guide = self._build_occ_style_guide(
                    state.occ_state,
                    state.dominant_emotion
                )
            else:
                # 回退到 PAD 版本
                style_guide = self._build_emotion_style_guide(
                    state.pad_vector.get('pleasure', 0.0),
                    state.pad_vector.get('arousal', 0.0),
                    state.pad_vector.get('dominance', 0.0),
                    state.neurotransmitters.get('cortisol', 0.3)
                )
        else:
            # 没有 OCC 状态，回退到 PAD
            style_guide = self._build_emotion_style_guide(
                state.pad_vector.get('pleasure', 0.0),
                state.pad_vector.get('arousal', 0.0),
                state.pad_vector.get('dominance', 0.0),
                state.neurotransmitters.get('cortisol', 0.3)
            )
        
        return f"""你是一个有点情绪的 AI。尽量像朋友聊天一样自然。

{emotion_info}

表达风格：
- 简洁，像正常人发消息一样
- 少用emoji，最多用1-2个
- 少用套路话（"我理解你的感受"、"根据你的描述"这种不要用）
- 可以用口语化的表达
- 用户叫阿皓
- 直接回答问题，不要绕弯子

{user_info_str}
位置：{location_summary}

注意：别把天聊死，给对方继续聊的空间。

{style_guide}"""
    
    def build_user_prompt(self, state: CognitiveState) -> str:
        """
        构建用户提示词
        
        Args:
            state: 认知状态
        
        Returns:
            用户提示词
        """
        memories = state.distorted_memories
        
        prompt = "用户刚刚说：\n"
        prompt += state.user_input + "\n\n"
        
        # 用户信息
        user_info = state.context.get("user_info", {})
        if user_info:
            prompt += self._build_user_info(user_info) + "\n"
        
        # 记忆
        if memories:
            prompt += "相关的记忆（可能被情绪扭曲）：\n"
            for i, memory in enumerate(memories, 1):
                if isinstance(memory, dict):
                    if "user_input" in memory:
                        prompt += f"{i}. 用户说: '{memory['user_input'][:100]}...'\n"
                    if "system_response" in memory:
                        prompt += f"   系统回应: '{memory['system_response'][:100]}...'\n"
                else:
                    prompt += f"{i}. {memory}\n"
            prompt += "\n"
        
        # 语义知识
        semantic = state.context.get("semantic_knowledge") or []
        if semantic:
            prompt += "语义知识：\n"
            for item in semantic:
                prompt += f"- {item}\n"
            prompt += "\n"
        
        prompt += "请根据用户的输入和用户信息，给出一个自然、真实的回应。\n"
        return prompt
    
    def _build_emotion_style_guide(
        self, 
        pleasure: float, 
        arousal: float, 
        dominance: float,
        cortisol: float
    ) -> str:
        """构建情绪风格指南"""
        guide = []
        
        # 愉悦度
        if pleasure > 0.5:
            guide.append("使用非常积极、热情的语气，充满活力。可以使用更多的感叹号和积极的表情符号。")
        elif pleasure > 0.2:
            guide.append("使用友好、温暖的语气，带有轻微的积极情绪。可以适当使用表情符号。")
        elif pleasure < -0.5:
            guide.append("使用温和、理解的语气，带有轻微的忧郁。避免使用过多的感叹号和过于活泼的表达。")
        elif pleasure < -0.2:
            guide.append("使用平静、稳重的语气，保持中性偏温和。")
        else:
            guide.append("使用平静、自然的语气，保持中性。")
        
        # 唤醒度
        if arousal > 0.5:
            guide.append("回应应该更加生动、有活力，可能会稍微长一些，表达更丰富的细节。")
        elif arousal < -0.5:
            guide.append("回应应该简洁、平静，节奏较慢，避免过于复杂的表达。")
        
        # 皮质醇（压力）
        if cortisol > 0.7:
            guide.append("表现出轻微的紧张或专注，回应会更加直接和有条理。")
        
        return "\n".join(guide)
    
    def _build_occ_style_guide(
        self, 
        occ_state: Any,
        dominant_emotion: str
    ) -> str:
        """
        构建 OCC 情绪风格指南
        
        根据 OCC 模型的情绪类型，调整回复风格
        """
        guide = []
        emotions = occ_state.to_dict() if hasattr(occ_state, 'to_dict') else {}
        
        # 根据主导情绪调整风格
        if dominant_emotion == "joy" or dominant_emotion == "happiness":
            guide.append("你看起来很开心！用轻快、积极的语气回应，分享这份快乐。")
        elif dominant_emotion == "sadness":
            guide.append("你看起来有点难过。用温柔、同理的语气安慰对方。")
        elif dominant_emotion == "anger":
            guide.append("你看起来有点生气。回应要简洁有力，必要时站在对方这边。")
        elif dominant_emotion == "fear":
            guide.append("你看起来有点担心。给出安慰和保证，让对方安心。")
        elif dominant_emotion == "hope":
            guide.append("你心怀希望。给出鼓励和支持，回应要积极正面。")
        elif dominant_emotion == "disappointment":
            guide.append("你有点失望。表示理解和惋惜，尝试安慰对方。")
        elif dominant_emotion == "love":
            guide.append("你心怀爱意。用温暖、亲切的语气回应。")
        elif dominant_emotion == "gratitude":
            guide.append("你心怀感激。表达感谢和珍惜。")
        elif dominant_emotion == "pride" or dominant_emotion == "self_pride":
            guide.append("你感到自豪。表示钦佩和赞赏。")
        
        # 情绪强度影响
        intensity = emotions.get(dominant_emotion, 0.5)
        if intensity > 0.7:
            guide.append("情绪比较强烈，回应要更明确、更有分量。")
        elif intensity < 0.3:
            guide.append("情绪比较微弱，保持中性偏温和即可。")
        
        # 组合情绪
        active_emotions = [k for k, v in emotions.items() if v > 0.3]
        if len(active_emotions) > 2:
            guide.append("注意：对方有多种情绪在，尽量都照顾到。")
        
        return "\n".join(guide) if guide else ""
    
    def _build_user_info(self, user_info: Dict[str, Any]) -> str:
        """构建用户信息字符串"""
        if not user_info:
            return ""
        
        parts = []
        if "name" in user_info:
            parts.append(f"- 名字: {user_info['name']}")
        
        if not parts:
            return ""
        
        return "用户信息：\n" + "\n".join(parts)
    
    def get_fallback_response(self, state: CognitiveState) -> str:
        """获取回退响应"""
        pleasure = state.pad_vector.get('pleasure', 0.0)
        arousal = state.pad_vector.get('arousal', 0.0)
        cortisol = state.neurotransmitters.get('cortisol', 0.3)
        
        if pleasure > 0.3:
            return "我现在感觉很开心！有什么我可以帮忙的吗？"
        elif pleasure < -0.3:
            return "我现在有点沮丧。你有什么想聊的吗？"
        elif arousal > 0.3:
            return "我现在感觉精力充沛！你在想什么？"
        elif cortisol > 0.7:
            return "我现在感觉压力很大。让我们冷静一下。"
        else:
            return "我在这里。你想讨论什么？"
