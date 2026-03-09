"""
OpenAPI 架构自动生成
"""

from typing import Dict, Any, Optional


def generate_openapi_spec(
    title: str = "Limbic-Flow API",
    version: str = "1.0.0",
    description: str = ""
) -> Dict[str, Any]:
    """生成 OpenAPI 规范"""
    
    return {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": version,
            "description": description
        },
        "servers": [
            {"url": "http://localhost:8001", "description": "本地开发"}
        ],
        "paths": {
            "/process": {
                "post": {
                    "summary": "处理用户输入",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "user_input": {"type": "string"},
                                        "context": {"type": "object"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "成功",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            "/emotion/current": {
                "get": {
                    "summary": "获取当前情绪",
                    "responses": {
                        "200": {"description": "成功"}
                    }
                }
            },
            "/config": {
                "get": {"summary": "获取配置"},
                "post": {"summary": "更新配置"}
            }
        }
    }


def generate_schema_from_model(model_class) -> Dict:
    """从模型类生成 Schema"""
    properties = {}
    required = []
    
    for name in dir(model_class):
        if name.startswith('_'):
            continue
        attr = getattr(model_class, name, None)
        if callable(attr):
            continue
        
        field_type = type(attr).__name__
        if isinstance(attr, int):
            field_type = "integer"
        elif isinstance(attr, float):
            field_type = "number"
        elif isinstance(attr, str):
            field_type = "string"
        elif isinstance(attr, bool):
            field_type = "boolean"
        
        properties[name] = {"type": field_type}
    
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }
