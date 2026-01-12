import sqlite3
import json
import time
from typing import List, Dict, Any

class Amygdala:
    """
    杏仁核模块 - 存储情绪状态日志和生理指标曲线
    """
    
    def __init__(self, db_path: str = "amygdala.db"):
        """
        初始化杏仁核
        
        Args:
            db_path: SQLite数据库路径
        """
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """
        初始化数据库表结构
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建状态日志表
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
        
        conn.commit()
        conn.close()
    
    def log_state(self, state: Dict[str, Any], context: str = None):
        """
        记录情绪状态
        
        Args:
            state: 情绪状态字典
            context: 上下文信息
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO state_log (timestamp, pleasure, arousal, dominance, dopamine, cortisol, context)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            state.get("timestamp", time.time()),
            state.get("pleasure", 0.0),
            state.get("arousal", 0.0),
            state.get("dominance", 0.0),
            state.get("dopamine", 0.5),
            state.get("cortisol", 0.3),
            json.dumps(context) if context else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_state_history(self, start_time: float = None, end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        获取状态历史
        
        Args:
            start_time: 开始时间戳
            end_time: 结束时间戳
            limit: 返回记录数量限制
        
        Returns:
            List[Dict[str, Any]]: 状态历史记录
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM state_log WHERE 1=1"
        params = []
        
        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)
        
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "timestamp": row[1],
                "pleasure": row[2],
                "arousal": row[3],
                "dominance": row[4],
                "dopamine": row[5],
                "cortisol": row[6],
                "context": json.loads(row[7]) if row[7] else None
            })
        
        conn.close()
        return result
    
    def get_latest_state(self) -> Dict[str, Any]:
        """
        获取最新的状态
        
        Returns:
            Dict[str, Any]: 最新的情绪状态
        """
        history = self.get_state_history(limit=1)
        return history[0] if history else {
            "timestamp": time.time(),
            "pleasure": 0.0,
            "arousal": 0.0,
            "dominance": 0.0,
            "dopamine": 0.5,
            "cortisol": 0.3
        }