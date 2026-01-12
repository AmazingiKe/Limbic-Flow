from typing import List, Union, Dict, Any
from openai import OpenAI
from limbic_flow.core.ai.base import BaseLLM, LLMConfig, LLMResponse, Message


class OpenAILLM(BaseLLM):
    """
    OpenAI LLM 适配器
    
    支持的模型：
    - gpt-4-turbo-preview
    - gpt-4
    - gpt-3.5-turbo
    
    特性：
    - 完全兼容 OpenAI API v1
    - 支持自定义 base_url（可用于兼容其他 OpenAI 兼容的 API）
    - 支持流式输出（可选）
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 OpenAI LLM
        
        Args:
            config: LLM 配置，必须包含 api_key
        """
        if not config.api_key:
            raise ValueError("OpenAI API Key 不能为空")
        super().__init__(config)

    def _initialize_client(self):
        """
        初始化 OpenAI 客户端
        """
        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )

    def chat(
        self,
        messages: List[Union[Message, Dict[str, str]]],
        **kwargs
    ) -> LLMResponse:
        """
        调用 OpenAI Chat API
        
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
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=normalized_messages,
                temperature=params.get("temperature"),
                max_tokens=params.get("max_tokens"),
                timeout=params.get("timeout")
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None,
                raw_response=response.model_dump()
            )
        except Exception as e:
            raise Exception(f"OpenAI API 调用失败: {str(e)}") from e
