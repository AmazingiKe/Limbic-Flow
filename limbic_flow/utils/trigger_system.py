"""
触发词系统 - 关键词检测与响应

[设计]
- 独立于病理模块
- 可配置的触发规则
- 支持多种触发类型（关键词、正则、语义）
- 事件驱动
"""

import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import random


class TriggerType(Enum):
    """触发类型"""
    KEYWORD = "keyword"      # 关键词匹配
    REGEX = "regex"         # 正则匹配
    SEMANTIC = "semantic"   # 语义匹配（需要embedding）
    EMOTION = "emotion"     # 情绪触发


@dataclass
class TriggerRule:
    """触发规则"""
    name: str
    type: TriggerType
    pattern: str  # 关键词或正则
    response_template: str  # 响应模板
    weight: float = 1.0  # 权重
    cooldown: float = 60.0  # 冷却时间（秒）
    enabled: bool = True
    
    def matches(self, text: str) -> bool:
        """检查是否匹配"""
        if not self.enabled:
            return False
        
        text_lower = text.lower()
        pattern_lower = self.pattern.lower()
        
        if self.type == TriggerType.KEYWORD:
            return pattern_lower in text_lower
        elif self.type == TriggerType.REGEX:
            return bool(re.search(self.pattern, text, re.IGNORECASE))
        
        return False


@dataclass
class TriggerEvent:
    """触发事件"""
    rule: TriggerRule
    matched_text: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__("time").time())


class TriggerSystem:
    """
    触发词系统
    
    [用途]
    - 关键词自动回复
    - 敏感词检测
    - 自定义对话触发
    - 与病理模块解耦
    """
    
    def __init__(self):
        self.rules: List[TriggerRule] = []
        self._last_trigger_time: Dict[str, float] = {}
        self._event_handlers: List[Callable[[TriggerEvent], None]] = []
        
        # 默认规则
        self._init_default_rules()
    
    def _init_default_rules(self):
        """初始化默认规则"""
        # 问候
        self.add_rule(TriggerRule(
            name="greeting",
            type=TriggerType.KEYWORD,
            pattern="你好|hello|hi|嗨",
            response_template="你好呀！有什么想聊的吗？",
            weight=1.0
        ))
        
        # 感谢
        self.add_rule(TriggerRule(
            name="thanks",
            type=TriggerType.KEYWORD,
            pattern="谢谢|感谢|thanks",
            response_template="不客气！很高兴能帮到你~",
            weight=1.0
        ))
        
        # 再见
        self.add_rule(TriggerRule(
            name="goodbye",
            type=TriggerType.KEYWORD,
            pattern="再见|bye|拜拜",
            response_template="再见！有空再聊~",
            weight=1.0
        ))
        
        # 询问情绪
        self.add_rule(TriggerRule(
            name="ask_mood",
            type=TriggerType.KEYWORD,
            pattern="你感觉怎么样|你心情好吗",
            response_template="我现在的状态嘛...{mood_description}",
            weight=1.0
        ))
    
    def add_rule(self, rule: TriggerRule) -> None:
        """添加触发规则"""
        self.rules.append(rule)
    
    def remove_rule(self, name: str) -> None:
        """移除规则"""
        self.rules = [r for r in self.rules if r.name != name]
    
    def enable_rule(self, name: str) -> None:
        """启用规则"""
        for rule in self.rules:
            if rule.name == name:
                rule.enabled = True
    
    def disable_rule(self, name: str) -> None:
        """禁用规则"""
        for rule in self.rules:
            if rule.name == name:
                rule.enabled = False
    
    def check(self, text: str, context: Dict[str, Any] = None) -> Optional[TriggerEvent]:
        """
        检查文本是否触发规则
        
        Args:
            text: 输入文本
            context: 上下文（可用于填充模板）
        
        Returns:
            TriggerEvent 或 None
        """
        context = context or {}
        
        # 按权重排序
        sorted_rules = sorted(
            [r for r in self.rules if r.enabled],
            key=lambda r: r.weight,
            reverse=True
        )
        
        for rule in sorted_rules:
            # 检查冷却时间
            if rule.name in self._last_trigger_time:
                import time
                elapsed = time.time() - self._last_trigger_time[rule.name]
                if elapsed < rule.cooldown:
                    continue
            
            # 检查匹配
            if rule.matches(text):
                # 记录触发时间
                import time
                self._last_trigger_time[rule.name] = time.time()
                
                # 生成事件
                event = TriggerEvent(
                    rule=rule,
                    matched_text=text,
                    context=context
                )
                
                # 通知处理器
                self._notify_handlers(event)
                
                return event
        
        return None
    
    def respond(self, event: TriggerEvent, emotion_state: Dict[str, Any] = None) -> str:
        """
        生成响应
        
        Args:
            event: 触发事件
            emotion_state: 当前情绪状态（可选）
        
        Returns:
            响应文本
        """
        template = event.rule.response_template
        
        # 填充情绪状态
        if emotion_state and "{mood_description}" in template:
            from limbic_flow.utils.emotion_analyzer import quick_analyze
            analysis = quick_analyze(emotion_state)
            template = template.replace("{mood_description}", analysis.internal_monologue)
        
        return template
    
    def on_trigger(self, handler: Callable[[TriggerEvent], None]) -> None:
        """注册触发事件处理器"""
        self._event_handlers.append(handler)
    
    def _notify_handlers(self, event: TriggerEvent) -> None:
        """通知所有处理器"""
        for handler in self._event_handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Trigger handler error: {e}")


class TraumaTriggerSystem(TriggerSystem):
    """
    创伤触发系统 - 用于 PTSD 病理
    
    继承 TriggerSystem，添加创伤记忆相关功能
    """
    
    def __init__(self):
        super().__init__()
        self.trauma_memories: List[Dict[str, Any]] = []
        
        # 添加默认创伤触发词
        self._init_trauma_triggers()
    
    def _init_trauma_triggers(self):
        """初始化创伤触发词"""
        trauma_keywords = [
            "去世", "死亡", "车祸", "事故", "伤害",
            "fire", "crash", "death", "accident", "trauma",
            "害怕", "恐惧", "阴影"
        ]
        
        for keyword in trauma_keywords:
            self.add_rule(TriggerRule(
                name=f"trauma_{keyword}",
                type=TriggerType.KEYWORD,
                pattern=keyword,
                response_template="",  # 不使用模板，直接返回创伤记忆
                weight=2.0,  # 高权重
                cooldown=300  # 5分钟冷却
            ))
    
    def add_trauma_memory(self, memory: Dict[str, Any]) -> None:
        """添加创伤记忆"""
        self.trauma_memories.append(memory)
    
    def get_trauma_response(self, event: TriggerEvent) -> List[Dict[str, Any]]:
        """
        获取创伤响应
        
        Args:
            event: 触发事件
        
        Returns:
            创伤记忆列表
        """
        if not self.trauma_memories:
            return []
        
        # 随机选择1-3条创伤记忆
        num_memories = min(len(self.trauma_memories), random.randint(1, 3))
        return random.sample(self.trauma_memories, num_memories)


# 全局实例
_default_trigger_system: Optional[TriggerSystem] = None

def get_trigger_system() -> TriggerSystem:
    """获取默认触发系统"""
    global _default_trigger_system
    if _default_trigger_system is None:
        _default_trigger_system = TriggerSystem()
    return _default_trigger_system
