"""
配置管理系统 - JSON 驱动的配置

参考 AstrBot 设计:
- 统一的配置管理
- 支持热重载
- 多环境配置
"""

import json
import os
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """
    配置管理器
    
    支持:
    - JSON 文件配置
    - 环境变量覆盖
    - 默认值
    - 热重载
    """
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = config_path
        self._config: Dict = {}
        self._defaults: Dict = {}
        self.load()
    
    def load(self):
        """加载配置"""
        path = Path(self.config_path)
        
        # 创建默认配置目录
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载或创建配置
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            self._config = self._defaults.copy()
            self.save()
    
    def save(self):
        """保存配置"""
        path = Path(self.config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        优先级: 环境变量 > 配置文件 > 默认值
        """
        # 检查环境变量
        env_key = f"LIMBIC_{key.upper().replace('.', '_')}"
        if env_key in os.environ:
            return os.environ[env_key]
        
        # 检查配置文件
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        if value is not None:
            return value
        
        # 检查默认值
        value = self._defaults
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        target = self._config
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
        self.save()
    
    def update(self, data: Dict):
        """批量更新配置"""
        self._config.update(data)
        self.save()
    
    def reset(self):
        """重置为默认值"""
        self._config = self._defaults.copy()
        self.save()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self._config.copy()


# 全局默认配置
DEFAULT_CONFIG = {
    "system": {
        "debug": False,
        "log_level": "INFO",
        "language": "zh-CN"
    },
    "llm": {
        "provider": "mock",
        "model": "",
        "api_key": "",
        "base_url": "",
        "temperature": 0.8,
        "max_tokens": 2000
    },
    "emotion": {
        "enabled": True,
        "model": "occ",  # occ 或 pad
        "half_life": {
            "pleasure": 3600,
            "arousal": 1800,
            "dominance": 2700
        }
    },
    "memory": {
        "enabled": True,
        "max_tokens": 4000,
        "importance_threshold": 0.3
    },
    "personality": {
        "default": "gentle",
        "available": ["default", "gentle", "playful", "wise", "energetic"]
    },
    "pathology": {
        "enabled": False,
        "available": ["none", "depression", "alzheimer", "ptsd", "hsp"]
    },
    "web": {
        "host": "0.0.0.0",
        "port": 8001,
        "cors_enabled": True
    }
}


# 全局实例
_config: Optional[Config] = None


def get_config() -> Config:
    """获取全局配置实例"""
    global _config
    if _config is None:
        _config = Config("config/settings.json")
        _config._defaults = DEFAULT_CONFIG
    return _config


def init_config(config_path: str = "config/settings.json") -> Config:
    """初始化配置"""
    global _config
    _config = Config(config_path)
    _config._defaults = DEFAULT_CONFIG
    return _config
