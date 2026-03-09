"""
验证器 - 输入验证和清洗
"""

import re
from typing import Any, Optional


class Validator:
    """验证器"""
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str = "字段") -> str:
        """验证非空"""
        if not value or not value.strip():
            raise ValueError(f"{field_name}不能为空")
        return value.strip()
    
    @staticmethod
    def validate_length(value: str, min_len: int = 0, max_len: int = 1000, field_name: str = "字段") -> str:
        """验证长度"""
        if len(value) < min_len:
            raise ValueError(f"{field_name}长度不能少于{min_len}个字符")
        if len(value) > max_len:
            raise ValueError(f"{field_name}长度不能超过{max_len}个字符")
        return value
    
    @staticmethod
    def validate_range(value: float, min_val: float = 0.0, max_val: float = 1.0, field_name: str = "值") -> float:
        """验证范围"""
        if value < min_val or value > max_val:
            raise ValueError(f"{field_name}必须在{min_val}和{max_val}之间")
        return value
    
    @staticmethod
    def validate_email(email: str) -> str:
        """验证邮箱"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("邮箱格式不正确")
        return email
    
    @staticmethod
    def validate_url(url: str) -> str:
        """验证 URL"""
        pattern = r'^https?://[^\s]+$'
        if not re.match(pattern, url):
            raise ValueError("URL 格式不正确")
        return url
    
    @staticmethod
    def validate_api_key(key: str) -> str:
        """验证 API Key"""
        if not key or len(key) < 10:
            raise ValueError("API Key 格式不正确")
        return key


class Sanitizer:
    """清洗器"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """移除 HTML 标签"""
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """移除 SQL 注入风险"""
        dangerous = ['--', ';', 'DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT']
        result = text
        for word in dangerous:
            result = result.replace(word, '')
        return result
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """清理文件名"""
        # 移除非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 限制长度
        return filename[:255]
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """标准化空白字符"""
        return ' '.join(text.split())
    
    @staticmethod
    def remove_emoji(text: str) -> str:
        """移除 emoji"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", 
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)


def validate_config(config: dict) -> dict:
    """验证配置"""
    v = Validator()
    
    # LLM 配置
    if 'llm_provider' in config:
        valid_providers = ['mock', 'openai', 'deepseek', 'anthropic', 'ollama']
        if config['llm_provider'] not in valid_providers:
            raise ValueError(f"无效的 LLM 提供商: {config['llm_provider']}")
    
    # 情感模型
    if 'emotion_model' in config:
        valid_models = ['occ', 'pad']
        if config['emotion_model'] not in valid_models:
            raise ValueError(f"无效的情感模型: {config['emotion_model']}")
    
    return config
