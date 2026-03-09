"""
数据库连接池
"""

import sqlite3
from typing import Any, List, Dict, Optional
from contextlib import contextmanager


class Database:
    """数据库连接池"""
    
    def __init__(self, db_path: str = "limbic.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    created_at REAL,
                    last_active REAL
                )
            """)
            
            # 对话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at REAL,
                    title TEXT
                )
            """)
            
            # 消息表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    created_at REAL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            
            # 情绪记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emotions (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    pleasure REAL,
                    arousal REAL,
                    dominance REAL,
                    dopamine REAL,
                    cortisol REAL,
                    created_at REAL
                )
            """)
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """获取连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """执行 SQL"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor
    
    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[Dict]:
        """查询单条"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetch_all(self, sql: str, params: tuple = ()) -> List[Dict]:
        """查询多条"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]


# 全局数据库实例
db = Database()
