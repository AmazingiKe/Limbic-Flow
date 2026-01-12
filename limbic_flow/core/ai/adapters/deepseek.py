from typing import List, Union, Dict
from openai import OpenAI
from limbic_flow.core.ai.base import BaseLLM, LLMConfig, LLMResponse, Message


class DeepSeekLLM(BaseLLM):
    """
    DeepSeek LLM 适配器
    
    支持的模型：
    - deepseek-chat
    - deepseek-coder
    
    特性：
    - 使用 OpenAI 兼容的 API
    - 支持自定义 base_url
    - 性价比高，适合大规模使用
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 DeepSeek LLM
        
        Args:
            config: LLM 配置，必须包含 api_key
        """
        if not config.api_key:
            raise ValueError("DeepSeek API Key 不能为空")
        
        if not config.base_url:
            config.base_url = "https://api.deepseek.com/v1"
        
        super().__init__(config)

    def _initialize_client(self):
        """
        初始化 DeepSeek 客户端（使用 OpenAI 客户端）
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
        调用 DeepSeek Chat API
        
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
            raise Exception(f"DeepSeek API 调用失败: {str(e)}") from e
