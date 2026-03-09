"""
API接口模块
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class EmotionRequest:
    """情绪请求"""
    action: str
    params: Dict[str, Any]


@dataclass
class EmotionResponse:
    """情绪响应"""
    status: str
    data: Dict[str, Any]
    error: str = ""


class EmotionAPI:
    """情绪API"""
    
    def __init__(self, emotion_engine):
        self.engine = emotion_engine
    
    def handle_request(self, request: EmotionRequest) -> EmotionResponse:
        """处理请求"""
        try:
            if request.action == "get_emotion":
                return EmotionResponse(
                    status="success",
                    data=self.engine.get_state()
                )
            elif request.action == "set_emotion":
                self.engine.set_state(request.params)
                return EmotionResponse(status="success", data={})
            else:
                return EmotionResponse(
                    status="error",
                    data={},
                    error="Unknown action"
                )
        except Exception as e:
            return EmotionResponse(status="error", data={}, error=str(e))


class EmotionMiddleware:
    """情绪中间件"""
    
    def __init__(self):
        self.middlewares = []
    
    def add(self, middleware):
        self.middlewares.append(middleware)
    
    def process(self, data):
        for mw in self.middlewares:
            data = mw.process(data)
        return data


if __name__ == "__main__":
    api = EmotionAPI(None)
    req = EmotionRequest("get_emotion", {})
    print(api.handle_request(req))
