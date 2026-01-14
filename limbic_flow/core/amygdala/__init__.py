import sqlite3
import json
import time
from typing import List, Dict, Any
from limbic_flow.core.types import CognitiveState

class Amygdala:
    """
    [职责] 杏仁核 - 情绪中心与神经递质调节器
    [场景] 感知后调用，决定当前的化学状态（焦虑/兴奋）
    [可替换性] 可替换为不同的情绪模型
    """
    
    def __init__(self, db_path: str = "amygdala.db"):
        """
        初始化杏仁核
        
        Args:
            db_path: SQLite数据库路径
        """
        self.db_path = db_path
        self._initialize_db()

    def process(self, state: CognitiveState) -> CognitiveState:
        """
        [职责] 处理情绪反应，计算神经递质水平
        [场景] 感知之后，记忆检索之前
        """
        # 1. 计算累积压力 (Cumulative Pressure) -> 影响皮质醇 (Cortisol)
        # 读取最近的历史状态
        history = self.get_state_history(limit=5)
        cumulative_stress = 0.0
        
        for record in history:
            r_arousal = record.get('arousal', 0.0)
            r_pleasure = record.get('pleasure', 0.0)
            
            # 如果处于高唤醒且低愉悦状态（焦虑/愤怒），积累压力
            if r_arousal > 0.2 and r_pleasure < -0.2:
                cumulative_stress += 0.1
        
        # 基础皮质醇水平受当前 PAD 影响
        # High Arousal + Low Dominance -> Anxiety -> Cortisol Spike
        current_stress = 0.0
        if state.arousal > 0.3 and state.dominance < -0.2:
            current_stress = 0.2
            
        # 更新皮质醇 (限制在 0-1)
        state.cortisol = min(1.0, max(0.0, 0.3 + cumulative_stress + current_stress + state.environmental_pressure))
        
        # 2. 计算多巴胺 (Dopamine) - 奖励预期
        # High Pleasure + High Dominance -> Dopamine
        dopamine_boost = 0.0
        if state.pleasure > 0.3:
            dopamine_boost += 0.2
        if state.dominance > 0.3:
            dopamine_boost += 0.1
            
        state.dopamine = min(1.0, max(0.0, 0.5 + dopamine_boost))

        # 3. 记录状态到数据库
        self.log_state({
            "pleasure": state.pleasure,
            "arousal": state.arousal,
            "dominance": state.dominance,
            "dopamine": state.dopamine,
            "cortisol": state.cortisol,
            "timestamp": state.timestamp
        }, context=state.user_input)
        
        return state
    
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