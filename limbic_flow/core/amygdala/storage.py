"""
情绪记忆存储层 - 抽象化的记忆数据库接口

将存储实现与业务逻辑分离，便于:
- 切换不同的存储后端（SQLite, Redis, 文件等）
- 单独测试业务逻辑
- 修改存储实现不影响上层代码
"""

import json
import sqlite3
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class EmotionalMemory:
    """单条情绪记忆"""
    timestamp: float
    pleasure: float
    arousal: float
    dominance: float
    dopamine: float
    cortisol: float
    context: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "pleasure": self.pleasure,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "dopamine": self.dopamine,
            "cortisol": self.cortisol,
            "context": self.context
        }


class MemoryStore(ABC):
    """
    记忆存储抽象基类
    
    定义存储层的接口规范，不同实现只需实现这些方法
    """
    
    @abstractmethod
    def save(self, memory: EmotionalMemory) -> None:
        """保存一条记忆"""
        pass
    
    @abstractmethod
    def get_recent(self, limit: int = 100) -> List[EmotionalMemory]:
        """获取最近的记忆"""
        pass
    
    @abstractmethod
    def get_range(self, start_time: float, end_time: float, limit: int = 100) -> List[EmotionalMemory]:
        """获取时间范围内的记忆"""
        pass
    
    @abstractmethod
    def get_latest(self) -> Optional[EmotionalMemory]:
        """获取最新的一条记忆"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """关闭连接"""
        pass


class SQLiteMemoryStore(MemoryStore):
    """
    SQLite 实现的记忆存储
    
    使用 SQLite 作为存储后端，适合单机使用
    """
    
    def __init__(self, db_path: str = "amygdala.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS state_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    pleasure REAL NOT NULL,
                    arousal REAL NOT NULL,
                    dominance REAL NOT NULL,
                    dopamine REAL NOT NULL,
                    cortisol REAL NOT NULL,
                    context TEXT
                )
            """)
            # 创建索引加速查询
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON state_log(timestamp DESC)
            """)
            conn.commit()
    
    def save(self, memory: EmotionalMemory) -> None:
        """保存一条记忆"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO state_log (timestamp, pleasure, arousal, dominance, dopamine, cortisol, context)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.timestamp,
                memory.pleasure,
                memory.arousal,
                memory.dominance,
                memory.dopamine,
                memory.cortisol,
                json.dumps(memory.context) if memory.context else None
            ))
            conn.commit()
    
    def get_recent(self, limit: int = 100) -> List[EmotionalMemory]:
        """获取最近的记忆"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, pleasure, arousal, dominance, dopamine, cortisol, context
                FROM state_log
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            return self._rows_to_memories(cursor.fetchall())
    
    def get_range(self, start_time: float, end_time: float, limit: int = 100) -> List[EmotionalMemory]:
        """获取时间范围内的记忆"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, pleasure, arousal, dominance, dopamine, cortisol, context
                FROM state_log
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (start_time, end_time, limit))
            return self._rows_to_memories(cursor.fetchall())
    
    def get_latest(self) -> Optional[EmotionalMemory]:
        """获取最新的一条记忆"""
        memories = self.get_recent(limit=1)
        return memories[0] if memories else None
    
    def _rows_to_memories(self, rows: List[tuple]) -> List[EmotionalMemory]:
        """将数据库行转换为记忆对象"""
        result = []
        for row in rows:
            result.append(EmotionalMemory(
                timestamp=row[0],
                pleasure=row[1],
                arousal=row[2],
                dominance=row[3],
                dopamine=row[4],
                cortisol=row[5],
                context=json.loads(row[6]) if row[6] else None
            ))
        return result
    
    def close(self) -> None:
        """关闭连接（SQLite不需要显式关闭）"""
        pass


class InMemoryMemoryStore(MemoryStore):
    """
    内存实现的记忆存储
    
    适合测试或不需要持久化的场景
    """
    
    def __init__(self):
        self._memories: List[EmotionalMemory] = []
    
    def save(self, memory: EmotionalMemory) -> None:
        self._memories.append(memory)
    
    def get_recent(self, limit: int = 100) -> List[EmotionalMemory]:
        sorted_memories = sorted(self._memories, key=lambda m: m.timestamp, reverse=True)
        return sorted_memories[:limit]
    
    def get_range(self, start_time: float, end_time: float, limit: int = 100) -> List[EmotionalMemory]:
        filtered = [m for m in self._memories if start_time <= m.timestamp <= end_time]
        sorted_filtered = sorted(filtered, key=lambda m: m.timestamp, reverse=True)
        return sorted_filtered[:limit]
    
    def get_latest(self) -> Optional[EmotionalMemory]:
        if not self._memories:
            return None
        return max(self._memories, key=lambda m: m.timestamp)
    
    def clear(self) -> None:
        """清空所有记忆"""
        self._memories.clear()
    
    def close(self) -> None:
        pass
