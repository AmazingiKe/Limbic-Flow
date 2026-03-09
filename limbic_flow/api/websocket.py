"""
WebSocket 支持
"""

from typing import Callable
import asyncio
import json


class WebSocketManager:
    """WebSocket 管理器"""
    
    def __init__(self):
        self.active_connections = set()
    
    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket):
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass
    
    async def send_personal(self, websocket, message: dict):
        await websocket.send_json(message)


ws_manager = WebSocketManager()
