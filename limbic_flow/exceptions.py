"""
错误处理 - 统一异常定义
"""

from typing import Optional, Any


class LimbicError(Exception):
    """基础异常"""
    code: int = 1000
    message: str = "未知错误"
    
    def __init__(self, message: str = None, **kwargs):
        self.message = message or self.message
        self.extra = kwargs
        super().__init__(self.message)


class ConfigError(LimbicError):
    """配置错误"""
    code = 2001
    message = "配置错误"


class LLMError(LimbicError):
    """LLM 调用错误"""
    code = 3001
    message = "LLM 调用失败"


class LLMAuthError(LLMError):
    """LLM 认证错误"""
    code = 3002
    message = "LLM 认证失败"


class LLMQuotaError(LLMError):
    """LLM 配额错误"""
    code = 3003
    message = "LLM 配额不足"


class MemoryError(LimbicError):
    """记忆错误"""
    code = 4001
    message = "记忆操作失败"


class EmotionError(LimbicError):
    """情绪处理错误"""
    code = 5001
    message = "情绪处理错误"


class PipelineError(LimbicError):
    """Pipeline 错误"""
    code = 6001
    message = "Pipeline 执行错误"


class ValidationError(LimbicError):
    """验证错误"""
    code = 7001
    message = "验证失败"


class RateLimitError(LimbicError):
    """限流错误"""
    code = 8001
    message = "请求过于频繁"


class ErrorHandler:
    """错误处理器"""
    
    @staticmethod
    def handle(error: Exception) -> dict:
        """处理错误"""
        if isinstance(error, LimbicError):
            return {
                "error": error.code,
                "message": error.message,
                "extra": error.extra
            }
        
        return {
            "error": 1000,
            "message": str(error),
            "type": type(error).__name__
        }
    
    @staticmethod
    def is_retryable(error: Exception) -> bool:
        """检查是否可重试"""
        retryable_codes = [3001, 5001, 6001]
        
        if isinstance(error, LimbicError):
            return error.code in retryable_codes
        
        return False


def handle_error(error: Exception) -> dict:
    """便捷错误处理函数"""
    return ErrorHandler.handle(error)
