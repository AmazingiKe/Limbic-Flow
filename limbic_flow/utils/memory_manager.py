"""
记忆管理系统 - 参考 AstrBot 的自学习 + 上下文压缩

功能:
- 长期记忆存储
- 上下文自动压缩
- 用户画像学习
- 对话风格自适应
"""

import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import numpy as np


@dataclass
class Memory:
    """记忆条目"""
    id: str
    content: str
    timestamp: float
    importance: float = 0.5  # 重要性 [0, 1]
    access_count: int = 0   # 访问次数
    keywords: List[str] = field(default_factory=list)
    embedding: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp,
            "importance": self.importance,
            "access_count": self.access_count,
            "keywords": self.keywords
        }


@dataclass  
class UserProfile:
    """用户画像 - 随对话学习"""
    name: Optional[str] = None
    interests: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    conversation_style: str = "normal"  # normal, formal, casual
    topics: List[str] = field(default_factory=list)
    last_seen: float = 0
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "interests": self.interests,
            "preferences": self.preferences,
            "conversation_style": self.conversation_style,
            "topics": self.topics,
            "last_seen": self.last_seen
        }


class MemoryManager:
    """
    记忆管理系统
    
    参考 AstrBot 设计:
    - 自动上下文压缩
    - 用户画像学习
    - 记忆重要性排序
    """
    
    def __init__(self, storage_path: str = "memory_store.json", max_tokens: int = 4000):
        self.storage_path = storage_path
        self.max_tokens = max_tokens
        self.memories: List[Memory] = []
        self.user_profiles: Dict[str, UserProfile] = {}
        self._load()
    
    def _load(self):
        """从文件加载"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.memories = [Memory(**m) for m in data.get('memories', [])]
                self.user_profiles = {
                    k: UserProfile(**v) for k, v in data.get('user_profiles', {}).items()
                }
        except FileNotFoundError:
            pass
    
    def _save(self):
        """保存到文件"""
        data = {
            "memories": [m.to_dict() for m in self.memories],
            "user_profiles": {k: v.to_dict() for k, v in self.user_profiles.items()}
        }
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_memory(
        self, 
        content: str, 
        importance: float = 0.5,
        keywords: List[str] = None,
        user_id: str = "default"
    ):
        """添加新记忆"""
        memory = Memory(
            id=f"mem_{int(time.time() * 1000)}",
            content=content,
            timestamp=time.time(),
            importance=importance,
            keywords=keywords or self._extract_keywords(content)
        )
        self.memories.append(memory)
        self._save()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """简单的关键词提取"""
        # 实际应该用 NLP，这里简化
        words = text.split()
        return [w for w in words if len(w) > 2][:5]
    
    def retrieve(
        self, 
        query: str, 
        limit: int = 5,
        user_id: str = "default"
    ) -> List[Memory]:
        """检索记忆 - 基于重要性和时间"""
        # 计算相关性分数
        query_keywords = set(self._extract_keywords(query))
        
        scored = []
        for mem in self.memories:
            # 关键词匹配
            keyword_score = len(query_keywords & set(mem.keywords)) / max(1, len(query_keywords))
            
            # 重要性分数
            importance_score = mem.importance
            
            # 时间衰减 (新记忆权重更高)
            hours_ago = (time.time() - mem.timestamp) / 3600
            recency_score = 1.0 / (1.0 + hours_ago * 0.1)
            
            # 访问次数
            access_score = min(1.0, mem.access_count / 10)
            
            total_score = (
                keyword_score * 0.3 + 
                importance_score * 0.3 + 
                recency_score * 0.25 + 
                access_score * 0.15
            )
            
            scored.append((total_score, mem))
        
        # 排序返回
        scored.sort(key=lambda x: x[0], reverse=True)
        
        # 更新访问计数
        for _, mem in scored[:limit]:
            mem.access_count += 1
        
        return [m for _, m in scored[:limit]]
    
    def compress_context(
        self, 
        messages: List[Dict], 
        max_tokens: int = None
    ) -> List[Dict]:
        """
        上下文压缩 - 保留关键信息
        
        策略:
        1. 保留最近 N 条消息
        2. 提取并保留高重要性记忆
        3. 合并相似内容
        """
        max_tokens = max_tokens or self.max_tokens
        
        # 估算 token (简单按字符/4)
        total_tokens = sum(len(m.get('content', '')) for m in messages) // 4
        
        if total_tokens <= max_tokens:
            return messages
        
        # 压缩策略
        compressed = []
        
        # 1. 保留系统提示（如果有）
        system_msgs = [m for m in messages if m.get('role') == 'system']
        compressed.extend(system_msgs)
        
        # 2. 保留最近 10 条
        user_msgs = [m for m in messages if m.get('role') != 'system']
        recent = user_msgs[-10:]
        
        # 3. 计算需要多少历史
        current_tokens = sum(len(m.get('content', '')) for m in compressed + recent) // 4
        remaining = max_tokens - current_tokens
        
        # 4. 添加重要记忆
        important_memories = [
            m.content for m in sorted(self.memories, key=lambda x: x.importance, reverse=True)[:3]
        ]
        
        for mem in important_memories:
            mem_tokens = len(mem) // 4
            if current_tokens + mem_tokens <= max_tokens:
                compressed.append({
                    "role": "system",
                    "content": f"【重要记忆】{mem}"
                })
                current_tokens += mem_tokens
        
        compressed.extend(recent)
        
        return compressed
    
    def learn_user_profile(self, user_id: str, message: str, response: str = None):
        """学习用户画像"""
        profile = self.user_profiles.get(user_id, UserProfile())
        
        # 更新最后活跃时间
        profile.last_seen = time.time()
        
        # 提取名字
        if not profile.name:
            import re
            patterns = [
                r"我叫(.*?)[，。！？]",
                r"我的名字是(.*?)[，。！？]",
            ]
            for pattern in patterns:
                match = re.search(pattern, message)
                if match:
                    profile.name = match.group(1).strip()
                    break
        
        # 提取兴趣关键词
        interest_words = ["喜欢", "感兴趣", "爱", " hobbies", "interest"]
        for word in interest_words:
            if word in message:
                idx = message.index(word)
                # 简单提取附近词
                start = max(0, idx - 10)
                end = min(len(message), idx + 10)
                profile.interests.append(message[start:end])
        
        # 学习对话风格
        if any(w in message for w in ["哈哈", "lol", "笑"]):
            profile.conversation_style = "casual"
        elif any(w in message for w in ["请", "您好", "谢谢"]):
            profile.conversation_style = "formal"
        
        self.user_profiles[user_id] = profile
        self._save()
    
    def get_context_for_prompt(self, user_id: str = "default") -> str:
        """获取用于 prompt 的上下文"""
        profile = self.user_profiles.get(user_id)
        if not profile:
            return ""
        
        context_parts = []
        
        if profile.name:
            context_parts.append(f"用户名字: {profile.name}")
        
        if profile.interests:
            context_parts.append(f"用户兴趣: {', '.join(set(profile.interests))}")
        
        if profile.conversation_style != "normal":
            context_parts.append(f"对话风格: {profile.conversation_style}")
        
        return " | ".join(context_parts) if context_parts else ""
    
    def reset(self):
        """重置所有记忆"""
        self.memories.clear()
        self.user_profiles.clear()
        self._save()


# 便捷函数
def create_memory_manager(storage_path: str = "memory_store.json") -> MemoryManager:
    """创建记忆管理器"""
    return MemoryManager(storage_path)
