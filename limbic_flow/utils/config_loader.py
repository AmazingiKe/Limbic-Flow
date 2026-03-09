"""
配置加载器
"""

import json
import os
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, Any] = {}
    
    def load_json(self, name: str) -> Dict:
        """加载 JSON 配置"""
        path = self.config_dir / f"{name}.json"
        if not path.exists():
            return {}
        
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.configs[name] = config
            return config
    
    def load_env(self, prefix: str = "LIMBIC_") -> Dict:
        """加载环境变量"""
        config = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config[key[len(prefix):].lower()] = value
        return config
    
    def merge(self, *configs: Dict) -> Dict:
        """合并配置"""
        result = {}
        for config in configs:
            result.update(config)
        return result
    
    def get(self, name: str, default: Any = None) -> Any:
        """获取配置"""
        return self.configs.get(name, default)
    
    def save_json(self, name: str, config: Dict):
        """保存 JSON 配置"""
        path = self.config_dir / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)


# 全局配置加载器
config_loader = ConfigLoader()
