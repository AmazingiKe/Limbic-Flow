import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from limbic_flow.core.ai.base import BaseLLM, LLMConfig
from limbic_flow.core.ai.adapters import (
    OpenAILLM,
    DeepSeekLLM,
    AnthropicLLM,
    OllamaLLM,
    MockLLM
)


class LLMFactory:
    """
    LLM 工厂类
    
    职责：
    - 根据配置创建对应的 LLM 实例
    - 统一管理环境变量配置
    - 提供便捷的 LLM 创建方法
    
    设计原则：
    - 单一职责：只负责创建 LLM 实例
    - 开闭原则：新增 LLM 只需注册，无需修改工厂逻辑
    - 依赖注入：通过环境变量注入配置
    
    使用示例：
        factory = LLMFactory()
        llm = factory.create_llm("openai")
        response = llm.chat_simple("Hello!")
    """

    LLM_REGISTRY = {
        "openai": OpenAILLM,
        "deepseek": DeepSeekLLM,
        "anthropic": AnthropicLLM,
        "ollama": OllamaLLM,
        "mock": MockLLM,
    }

    def __init__(self, env_file: Optional[str] = None):
        """
        初始化 LLM 工厂
        
        Args:
            env_file: .env 文件路径，默认为项目根目录的 .env
        """
        load_dotenv(env_file)
        self.default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "mock")

    def create_llm(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseLLM:
        """
        创建 LLM 实例
        
        Args:
            provider: LLM 提供商（openai, deepseek, anthropic, ollama）
                    如果为 None，使用环境变量 DEFAULT_LLM_PROVIDER
            model: 模型名称，如果为 None，使用环境变量中的默认模型
            **kwargs: 额外的配置参数
        
        Returns:
            BaseLLM: LLM 实例
        
        Raises:
            ValueError: 不支持的提供商或缺少必要配置时抛出异常
        """
        provider = provider or self.default_provider
        provider = provider.lower()

        if provider not in self.LLM_REGISTRY:
            raise ValueError(
                f"不支持的 LLM 提供商: {provider}。"
                f"支持的提供商: {list(self.LLM_REGISTRY.keys())}"
            )

        llm_class = self.LLM_REGISTRY[provider]
        config = self._get_config(provider, model, **kwargs)

        return llm_class(config)

    def _get_config(
        self,
        provider: str,
        model: Optional[str] = None,
        **kwargs
    ) -> LLMConfig:
        """
        获取 LLM 配置
        
        Args:
            provider: LLM 提供商
            model: 模型名称
            **kwargs: 额外的配置参数
        
        Returns:
            LLMConfig: LLM 配置对象
        """
        provider_upper = provider.upper()

        config = LLMConfig(
            model=model or os.getenv(f"{provider_upper}_MODEL"),
            api_key=os.getenv(f"{provider_upper}_API_KEY"),
            base_url=os.getenv(f"{provider_upper}_BASE_URL"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
            timeout=int(os.getenv("LLM_TIMEOUT", "30")),
        )

        config.extra_params = kwargs

        return config

    @classmethod
    def register_llm(cls, name: str, llm_class: type):
        """
        注册新的 LLM 提供商
        
        Args:
            name: 提供商名称
            llm_class: LLM 类（必须继承自 BaseLLM）
        
        Raises:
            TypeError: 如果 llm_class 不是 BaseLLM 的子类
        """
        if not issubclass(llm_class, BaseLLM):
            raise TypeError(f"{llm_class} 必须继承自 BaseLLM")

        cls.LLM_REGISTRY[name.lower()] = llm_class

    @classmethod
    def get_supported_providers(cls) -> list:
        """
        获取所有支持的 LLM 提供商
        
        Returns:
            list: 提供商名称列表
        """
        return list(cls.LLM_REGISTRY.keys())

    def create_openai_llm(self, **kwargs) -> OpenAILLM:
        """创建 OpenAI LLM 实例"""
        return self.create_llm("openai", **kwargs)

    def create_deepseek_llm(self, **kwargs) -> DeepSeekLLM:
        """创建 DeepSeek LLM 实例"""
        return self.create_llm("deepseek", **kwargs)

    def create_anthropic_llm(self, **kwargs) -> AnthropicLLM:
        """创建 Anthropic LLM 实例"""
        return self.create_llm("anthropic", **kwargs)

    def create_ollama_llm(self, **kwargs) -> OllamaLLM:
        """创建 Ollama LLM 实例"""
        return self.create_llm("ollama", **kwargs)

    def create_mock_llm(self, **kwargs) -> MockLLM:
        """创建 Mock LLM 实例"""
        return self.create_llm("mock", **kwargs)
