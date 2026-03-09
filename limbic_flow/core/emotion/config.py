"""
情绪配置文件
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class EmotionConfig:
    """情绪配置"""
    decay_rate: float = 0.1
    regulation_threshold: float = 0.7
    enable_pathology: bool = True


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.configs: Dict[str, EmotionConfig] = {}
        self._init_defaults()
    
    def _init_defaults(self):
        """初始化默认配置"""
        self.configs["default"] = EmotionConfig()
        self.configs["therapy"] = EmotionConfig(
            decay_rate=0.05,
            regulation_threshold=0.5
        )
    
    def get_config(self, name: str = "default") -> EmotionConfig:
        """获取配置"""
        return self.configs.get(name, self.configs["default"])
    
    def update_config(self, name: str, **kwargs):
        """更新配置"""
        if name not in self.configs:
            self.configs[name] = EmotionConfig()
        
        for key, value in kwargs.items():
            if hasattr(self.configs[name], key):
                setattr(self.configs[name], key, value)


if __name__ == "__main__":
    mgr = ConfigManager()
    cfg = mgr.get_config("therapy")
    print(f"Decay: {cfg.decay_rate}")
