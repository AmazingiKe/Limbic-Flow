"""
数据验证器
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field, validator


class LLMConfigSchema(BaseModel):
    """LLM 配置验证"""
    provider: str = Field(..., description="LLM 提供商")
    model: str = Field(default="", description="模型名称")
    api_key: str = Field(default="", description="API Key")
    base_url: str = Field(default="", description="Base URL")
    temperature: float = Field(default=0.8, ge=0, le=2)
    max_tokens: int = Field(default=2000, ge=1, le=10000)


class EmotionConfigSchema(BaseModel):
    """情感配置验证"""
    model: str = Field(default="occ")
    half_life_pleasure: int = Field(default=3600, ge=1)
    half_life_arousal: int = Field(default=1800, ge=1)
    half_life_dominance: int = Field(default=2700, ge=1)


class PersonalityConfigSchema(BaseModel):
    """人格配置验证"""
    name: str
    openness: float = Field(ge=0, le=1)
    conscientiousness: float = Field(ge=0, le=1)
    extraversion: float = Field(ge=0, le=1)
    agreeableness: float = Field(ge=0, le=1)
    neuroticism: float = Field(ge=0, le=1)


def validate_config(config: Dict[str, Any]) -> bool:
    """验证配置"""
    try:
        LLMConfigSchema(**config.get('llm', {}))
        EmotionConfigSchema(**config.get('emotion', {}))
        return True
    except Exception as e:
        print(f"配置验证失败: {e}")
        return False
