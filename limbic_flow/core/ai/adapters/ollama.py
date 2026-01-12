from typing import List, Union, Dict
from openai import OpenAI
from limbic_flow.core.ai.base import BaseLLM, LLMConfig, LLMResponse, Message


class OllamaLLM(BaseLLM):
    """
    Ollama LLM 适配器
    
    支持的模型：
    - llama2
    - mistral
    - codellama
    - 以及 Ollama 支持的所有模型
    
    特性：
    - 本地运行，无需 API Key
    - 完全免费
    - 支持自定义模型
    - 使用 OpenAI 兼容的 API
    """

    def __init__(self, config: LLMConfig):
        """
        初始化 Ollama LLM
        
        Args:
            config: LLM 配置，不需要 api_key
        """
        if not config.base_url:
            config.base_url = "http://localhost:11434/v1"
        
        super().__init__(config)

    def _initialize_client(self):
        """
        初始化 Ollama 客户端（使用 OpenAI 客户端）
        """
        self.client = OpenAI(
            api_key="ollama",
            base_url=self.config.base_url,
            timeout=self.config.timeout
        )

    def chat(
        self,
        messages: List[Union[Message, Dict[str, str]]],
        **kwargs
    ) -> LLMResponse:
        """
        调用 Ollama Chat API
        
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
            raise Exception(f"Ollama API 调用失败: {str(e)}") from e
