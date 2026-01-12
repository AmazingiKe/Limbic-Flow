from typing import List, Union, Dict
from limbic_flow.core.ai.base import BaseLLM, LLMConfig, LLMResponse, Message


class MockLLM(BaseLLM):
    """
    Mock LLM 适配器 - 用于测试和开发
    
    特性：
    - 无需 API Key
    - 返回预设的响应
    - 用于测试和开发阶段
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 Mock LLM
        
        Args:
            config: LLM 配置
        """
        super().__init__(config)

    def _initialize_client(self):
        """
        Mock LLM 不需要客户端
        """
        pass

    def chat(
        self,
        messages: List[Union[Message, Dict[str, str]]],
        **kwargs
    ) -> LLMResponse:
        """
        模拟聊天接口
        
        Args:
            messages: 消息列表
            **kwargs: 额外的参数（忽略）
        
        Returns:
            LLMResponse: 模拟的响应对象
        """
        # 获取最后一条用户消息
        user_message = ""
        for msg in reversed(messages):
            if isinstance(msg, Message):
                if msg.role.value == "user":
                    user_message = msg.content
                    break
            elif isinstance(msg, dict):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break

        # 根据用户消息生成简单的响应
        response_content = self._generate_mock_response(user_message)

        return LLMResponse(
            content=response_content,
            model=self.config.model or "mock-model",
            usage={
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(response_content.split()),
                "total_tokens": len(user_message.split()) + len(response_content.split())
            },
            raw_response={"mock": True}
        )

    def _generate_mock_response(self, user_message: str) -> str:
        """
        生成模拟响应
        
        Args:
            user_message: 用户消息
        
        Returns:
            str: 模拟响应
        """
        user_message_lower = user_message.lower()

        if "开心" in user_message_lower or "happy" in user_message_lower:
            return "听到你这么开心，我也感到很高兴！有什么我可以帮你的吗？"
        elif "伤心" in user_message_lower or "sad" in user_message_lower:
            return "我理解你的感受。有时候倾诉一下会好很多，你想聊聊吗？"
        elif "生气" in user_message_lower or "angry" in user_message_lower:
            return "我能感觉到你的愤怒。深呼吸，我们一起冷静一下。"
        elif "害怕" in user_message_lower or "scared" in user_message_lower:
            return "不要害怕，我在这里陪着你。告诉我发生了什么？"
        elif "累" in user_message_lower or "tired" in user_message_lower:
            return "辛苦了！休息一下很重要，有什么我可以帮你的吗？"
        elif "谢谢" in user_message_lower or "thank" in user_message_lower:
            return "不客气！能帮到你我很开心。"
        elif "你好" in user_message_lower or "hello" in user_message_lower:
            return "你好！很高兴见到你。今天过得怎么样？"
        elif "再见" in user_message_lower or "bye" in user_message_lower:
            return "再见！希望下次还能和你聊天。"
        else:
            return "我听到了。能多告诉我一些吗？"
