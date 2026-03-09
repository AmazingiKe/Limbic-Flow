"""
Pipeline 配置模块
"""

from dataclasses import dataclass, field
from typing import Optional, List, Any


@dataclass
class PipelineConfig:
    """
    Pipeline 配置 - 控制整个认知流程的行为
    """
    # LLM 配置
    llm_provider: str = None  # None = 使用默认
    
    # 记忆配置
    memory_limit: int = 5  # 每次检索的记忆数量
    memory_store_path: str = "./memory_store.json"
    
    # 情绪配置
    use_sensitive_emotion: bool = False  # 是否使用敏感型情绪配置
    
    # 病理配置
    enable_depression: bool = True
    enable_alzheimer: bool = False
    enable_ptsd: bool = False
    enable_hsp: bool = False
    depression_severity: float = 0.3
    alzheimer_severity: float = 0.5
    ptsd_severity: float = 0.5
    hsp_sensitivity: float = 0.5
    
    # 表达配置
    base_wpm: int = 60
    min_segment_length: int = 10
    max_segment_length: int = 50
    
    # 调试配置
    debug_mode: bool = False
    
    @staticmethod
    def relaxed() -> "PipelineConfig":
        """放松型配置 - 情绪稳定，衰减慢"""
        config = PipelineConfig()
        config.use_sensitive_emotion = False
        config.enable_depression = False
        config.enable_hsp = False
        return config
    
    @staticmethod
    def sensitive() -> "PipelineConfig":
        """敏感型配置 - 情绪波动大"""
        config = PipelineConfig()
        config.use_sensitive_emotion = True
        config.enable_depression = True
        config.enable_hsp = True
        config.depression_severity = 0.5
        config.hsp_sensitivity = 0.7
        return config
    
    @staticmethod
    def alzheimer_mode() -> "PipelineConfig":
        """阿尔茨海默模式配置"""
        config = PipelineConfig()
        config.enable_alzheimer = True
        config.alzheimer_severity = 0.7
        return config
