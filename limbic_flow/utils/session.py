"""
会话管理系统 - 对话状态管理
"""

import uuid
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Session:
    """会话"""
    id: str
    user_id: str
    created_at: float
    last_active: float
    messages: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        self.last_active = time.time()
    
    def get_messages(self, limit: int = None) -> List[Dict]:
        """获取消息"""
        if limit:
            return self.messages[-limit:]
        return self.messages
    
    def clear(self):
        """清空消息"""
        self.messages.clear()


class SessionManager:
    """会话管理器"""
    
    def __init__(self, max_sessions: int = 100, session_timeout: int = 3600):
        self.max_sessions = max_sessions
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Session] = {}
        self.user_sessions: Dict[str, str] = {}  # user_id -> session_id
    
    def create_session(self, user_id: str = "default") -> Session:
        """创建会话"""
        # 清理过期会话
        self._cleanup()
        
        session_id = str(uuid.uuid4())
        now = time.time()
        
        session = Session(
            id=session_id,
            user_id=user_id,
            created_at=now,
            last_active=now
        )
        
        self.sessions[session_id] = session
        self.user_sessions[user_id] = session_id
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        session = self.sessions.get(session_id)
        
        if session and self._is_valid(session):
            return session
        
        return None
    
    def get_or_create_session(self, session_id: str = None, user_id: str = "default") -> Session:
        """获取或创建会话"""
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
        
        # 检查用户是否有活跃会话
        if user_id in self.user_sessions:
            session = self.get_session(self.user_sessions[user_id])
            if session:
                return session
        
        return self.create_session(user_id)
    
    def _is_valid(self, session: Session) -> bool:
        """检查会话是否有效"""
        return (time.time() - session.last_active) < self.session_timeout
    
    def _cleanup(self):
        """清理过期会话"""
        now = time.time()
        
        # 清理过期会话
        expired = [
            sid for sid, s in self.sessions.items()
            if (now - s.last_active) > self.session_timeout
        ]
        
        for sid in expired:
            session = self.sessions.pop(sid)
            if session.user_id in self.user_sessions:
                del self.user_sessions[session.user_id]
        
        # 限制最大会话数
        if len(self.sessions) > self.max_sessions:
            oldest = min(self.sessions.values(), key=lambda s: s.last_active)
            self.delete_session(oldest.id)
    
    def delete_session(self, session_id: str):
        """删除会话"""
        if session_id in self.sessions:
            session = self.sessions.pop(session_id)
            if session.user_id in self.user_sessions:
                del self.user_sessions[session.user_id]
    
    def list_sessions(self) -> List[Dict]:
        """列出所有会话"""
        return [
            {
                "id": s.id,
                "user_id": s.user_id,
                "created_at": s.created_at,
                "last_active": s.last_active,
                "message_count": len(s.messages)
            }
            for s in self.sessions.values()
        ]


# 全局会话管理器
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """获取全局会话管理器"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
