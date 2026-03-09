"""
序列化工具
"""

import json
import pickle
from typing import Any, Dict
from pathlib import Path


class Serializer:
    """序列化器"""
    
    @staticmethod
    def to_json(obj: Any, indent: int = 2) -> str:
        """转为 JSON"""
        return json.dumps(obj, indent=indent, ensure_ascii=False, default=str)
    
    @staticmethod
    def from_json(text: str) -> Any:
        """从 JSON 解析"""
        return json.loads(text)
    
    @staticmethod
    def to_pickle(obj: Any) -> bytes:
        """转为 pickle"""
        return pickle.dumps(obj)
    
    @staticmethod
    def from_pickle(data: bytes) -> Any:
        """从 pickle 解析"""
        return pickle.loads(data)
    
    @staticmethod
    def save_json(obj: Any, path: str):
        """保存为 JSON 文件"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False, default=str)
    
    @staticmethod
    def load_json(path: str) -> Any:
        """从 JSON 文件加载"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


class DataExporter:
    """数据导出器"""
    
    @staticmethod
    def export_conversation(messages: list, path: str):
        """导出对话"""
        data = {
            "version": "1.0",
            "exported_at": str(Path(path).stat().st_mtime),
            "messages": messages
        }
        Serializer.save_json(data, path)
    
    @staticmethod
    def export_memory(memory_data: list, path: str):
        """导出记忆"""
        data = {
            "version": "1.0",
            "exported_at": str(Path(path).stat().st_mtime),
            "memories": memory_data
        }
        Serializer.save_json(data, path)


# 便捷函数
to_json = Serializer.to_json
from_json = Serializer.from_json
save_json = Serializer.save_json
load_json = Serializer.load_json
