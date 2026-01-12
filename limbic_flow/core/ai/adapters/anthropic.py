from typing import List, Union, Dict
from anthropic import Anthropic
from limbic_flow.core.ai.base import BaseLLM, LLMConfig, LLMResponse, Message, MessageRole


class AnthropicLLM(BaseLLM):
    """
    Anthropic LLM 适配器
    
    支持的模型：
    - claude-3-opus-20240229
    - claude-3-sonnet-20240229
    - claude-3-haiku-20240307
    
    特性：
    - 使用 Anthropic 官方 API
    - 支持 Claude 3 系列
    - 支持长上下文
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 Anthropic LLM
        
        Args:
            config: LLM 配置，必须包含 api_key
        """
        if not config.api_key:
            raise ValueError("Anthropic API Key 不能为空")
        super().__init__(config)

    def _initialize_client(self):
        """
        初始化 Anthropic 客户端
        """
        self.client = Anthropic(
            api_key=self.config.api_key,
            timeout=self.config.timeout
        )

    def chat(
        self,
        messages: List[Union[Message, Dict[str, str]]],
        **kwargs
    ) -> LLMResponse:
        """
        调用 Anthropic Messages API
        
        Args:
            messages: 消息列表
            **kwargs: 额外的参数（temperature, max_tokens 等）
        
        Returns:
            LLMResponse: LLM 响应对象
        
        Raises:
            Exception: API 调用失败时抛出异常
        """
        normalized_messages = self._normalize_messages(messages)
        params = self._merge_config(**kwargs)
        
        try:
            system_message = ""
            api_messages = []
            
            for msg in normalized_messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = self.client.messages.create(
                model=self.config.model,
                messages=api_messages,
                system=system_message if system_message else None,
                temperature=params.get("temperature"),
                max_tokens=params.get("max_tokens", 4096)
            )
            
            return LLMResponse(
                content=response.content[0].text,
                model=response.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                },
                raw_response=response.model_dump()
            )
        except Exception as e:
            raise Exception(f"Anthropic API 调用失败: {str(e)}") from e
