"""
Webhook 系统
"""

import asyncio
import aiohttp
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Webhook:
    """Webhook 配置"""
    url: str
    event: str
    secret: Optional[str] = None
    enabled: bool = True


class WebhookManager:
    """Webhook 管理器"""
    
    def __init__(self):
        self.webhooks: Dict[str, Webhook] = {}
        self.handlers: Dict[str, Callable] = {}
    
    def register(self, event: str, url: str, secret: Optional[str] = None):
        """注册 Webhook"""
        self.webhooks[event] = Webhook(url, event, secret)
    
    def on(self, event: str):
        """装饰器注册事件处理"""
        def decorator(func: Callable):
            self.handlers[event] = func
            return func
        return decorator
    
    async def trigger(self, event: str, data: Dict[str, Any]):
        """触发 Webhook"""
        if event not in self.webhooks:
            return
        
        webhook = self.webhooks[event]
        if not webhook.enabled:
            return
        
        # 调用本地处理
        if event in self.handlers:
            await self.handlers[event](data)
        
        # 发送 HTTP 请求
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(webhook.url, json=data)
        except Exception as e:
            print(f"Webhook 发送失败: {e}")
    
    def enable(self, event: str):
        if event in self.webhooks:
            self.webhooks[event].enabled = True
    
    def disable(self, event: str):
        if event in self.webhooks:
            self.webhooks[event].enabled = False


# 全局实例
webhook_manager = WebhookManager()
