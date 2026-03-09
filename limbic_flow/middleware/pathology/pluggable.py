"""
插件化病理中间件 - 从 JSON 加载规则

设计原则:
- 规则由 JSON 文件定义
- 支持运行时加载/卸载
- 灵活的条件-动作规则引擎
"""

import json
import re
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
from abc import ABC, abstractmethod


@dataclass
class PathologyRule:
    """病理规则"""
    type: str                    # 规则类型
    condition: Dict[str, Any]    # 触发条件
    action: str                  # 执行动作
    probability: float = 1.0     # 触发概率
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PathologyConfig:
    """病理配置"""
    enabled: bool = False
    name: str = ""
    description: str = ""
    rules: List[PathologyRule] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)


class RuleEngine:
    """
    规则引擎 - 执行条件-动作规则
    """
    
    def __init__(self):
        self.conditions: Dict[str, Callable] = {
            "emotion": self._check_emotion,
            "pleasure": self._check_pleasure,
            "arousal": self._check_arousal,
            "recency": self._check_recency,
            "trigger_word": self._check_trigger_word,
        }
        
        self.actions: Dict[str, Callable] = {
            "suppress": self._action_suppress,
            "reduce": self._action_reduce,
            "amplify": self._action_amplify,
            "block": self._action_block,
            "inject_trauma": self._action_inject_trauma,
            "gaussian_noise": self._action_gaussian_noise,
        }
    
    def evaluate(
        self, 
        rule: PathologyRule, 
        context: Dict[str, Any]
    ) -> bool:
        """
        评估规则是否满足条件
        
        Args:
            rule: 规则
            context: 上下文（情绪状态、记忆等）
        
        Returns:
            是否触发
        """
        # 随机概率检查
        import random
        if random.random() > rule.probability:
            return False
        
        # 检查每个条件
        for key, value in rule.condition.items():
            if key in self.conditions:
                if not self.conditions[key](value, context):
                    return False
            elif key == "trigger_word":
                # 特殊处理触发词
                if not self._check_trigger_word(value, context):
                    return False
        
        return True
    
    def execute(
        self, 
        rule: PathologyRule, 
        data: Any, 
        context: Dict[str, Any]
    ) -> Any:
        """
        执行规则动作
        
        Args:
            rule: 规则
            data: 待处理数据（记忆、查询等）
            context: 上下文
        
        Returns:
            处理后的数据
        """
        if rule.action in self.actions:
            return self.actions[rule.action](data, rule.parameters, context)
        return data
    
    # 条件检查器
    def _check_emotion(self, condition: Any, context: Dict[str, Any]) -> bool:
        emotion = context.get("emotion_state", {})
        emotion_type = condition.get("type") if isinstance(condition, dict) else condition
        threshold = condition.get("threshold", 0.3) if isinstance(condition, dict) else 0.3
        
        current = emotion.get(emotion_type, 0.0)
        return current > threshold
    
    def _check_pleasure(self, condition: Any, context: Dict[str, Any]) -> bool:
        emotion = context.get("emotion_state", {})
        threshold = condition.get("threshold", 0.0) if isinstance(condition, dict) else 0.0
        return emotion.get("pleasure", 0.0) > threshold
    
    def _check_arousal(self, condition: Any, context: Dict[str, Any]) -> bool:
        emotion = context.get("emotion_state", {})
        threshold = condition.get("threshold", 0.0) if isinstance(condition, dict) else 0.0
        return emotion.get("arousal", 0.0) > threshold
    
    def _check_recency(self, condition: Any, context: Dict[str, Any]) -> bool:
        import time
        memory = context.get("memory", {})
        recency = condition.get("recency", "<86400") if isinstance(condition, dict) else "<86400"
        
        # 解析时间条件
        if "<" in recency:
            max_seconds = int(recency.replace("<", ""))
            memory_time = memory.get("timestamp", 0)
            return (time.time() - memory_time) < max_seconds
        
        return True
    
    def _check_trigger_word(self, triggers: Any, context: Dict[str, Any]) -> bool:
        user_input = context.get("user_input", "").lower()
        
        if isinstance(triggers, str):
            triggers = [triggers]
        
        for trigger in triggers:
            if trigger.lower() in user_input:
                return True
        return False
    
    # 动作执行器
    def _action_suppress(self, data: Any, params: Dict, context: Dict) -> Any:
        """抑制/过滤"""
        return None  # 返回 None 表示过滤掉
    
    def _action_reduce(self, value: float, params: Dict, context: Dict) -> float:
        """降低强度"""
        factor = params.get("factor", 0.5)
        return value * factor
    
    def _action_amplify(self, value: float, params: Dict, context: Dict) -> float:
        """放大强度"""
        factor = params.get("factor", 1.5)
        return min(1.0, value * factor)
    
    def _action_block(self, data: Any, params: Dict, context: Dict) -> Any:
        """阻断"""
        return None
    
    def _action_inject_trauma(self, data: Any, params: Dict, context: Dict) -> Any:
        """注入创伤记忆"""
        trauma_memories = context.get("trauma_memories", [])
        if trauma_memories:
            import random
            selected = random.sample(trauma_memories, min(3, len(trauma_memories)))
            return selected + (data if isinstance(data, list) else [data])
        return data
    
    def _action_gaussian_noise(self, vector: Any, params: Dict, context: Dict) -> Any:
        """添加高斯噪声"""
        import numpy as np
        if hasattr(vector, 'shape'):
            std = params.get("std", 0.2)
            noise = np.random.normal(0, std, vector.shape)
            return vector + noise
        return vector


class PluggablePathologyMiddleware:
    """
    可插拔病理中间件
    
    特点:
    - 从 JSON 文件加载病理规则
    - 支持动态启用/禁用
    - 可运行时修改参数
    """
    
    def __init__(self, config_path: str = None):
        self.rule_engine = RuleEngine()
        self.pathologies: Dict[str, PathologyConfig] = {}
        self.enabled_pathologies: set = set()
        
        if config_path:
            self.load_from_file(config_path)
    
    def load_from_file(self, config_path: str):
        """从 JSON 文件加载配置"""
        path = Path(config_path)
        if not path.exists():
            # 尝试默认路径
            path = Path(__file__).parent.parent.parent / "config" / "pathology.json"
        
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            self._parse_config(config)
    
    def _parse_config(self, config: Dict):
        """解析配置"""
        pathologies = config.get("pathologies", {})
        
        for name, data in pathologies.items():
            pathology = PathologyConfig(
                enabled=data.get("enabled", False),
                name=data.get("name", name),
                description=data.get("description", ""),
                rules=[
                    PathologyRule(
                        type=r.get("type", ""),
                        condition=r.get("condition", {}),
                        action=r.get("action", ""),
                        probability=r.get("probability", 1.0),
                        parameters=r.get("parameters", {})
                    )
                    for r in data.get("rules", [])
                ],
                parameters=data.get("parameters", {})
            )
            self.pathologies[name] = pathology
            
            if pathology.enabled:
                self.enabled_pathologies.add(name)
    
    def enable(self, name: str):
        """启用病理"""
        if name in self.pathologies:
            self.enabled_pathologies.add(name)
            self.pathologies[name].enabled = True
    
    def disable(self, name: str):
        """禁用病理"""
        self.enabled_pathologies.discard(name)
        if name in self.pathologies:
            self.pathologies[name].enabled = False
    
    def set_parameter(self, name: str, key: str, value: Any):
        """设置病理参数"""
        if name in self.pathologies:
            self.pathologies[name].parameters[key] = value
    
    def process(self, state: Any) -> Any:
        """
        处理状态，应用病理规则
        
        Args:
            state: CognitiveState
        
        Returns:
            处理后的状态
        """
        # 构建上下文
        context = self._build_context(state)
        
        # 处理每个启用的病理
        for name in self.enabled_pathologies:
            pathology = self.pathologies.get(name)
            if not pathology:
                continue
            
            # 应用规则
            for rule in pathology.rules:
                if self.rule_engine.evaluate(rule, context):
                    # 执行动作
                    pass  # 实际执行逻辑
        
        return state
    
    def _build_context(self, state: Any) -> Dict:
        """构建上下文"""
        return {
            "emotion_state": {
                "pleasure": state.pad_vector.get("pleasure", 0.0),
                "arousal": state.pad_vector.get("arousal", 0.0),
                "dominance": state.pad_vector.get("dominance", 0.0),
            },
            "user_input": getattr(state, "user_input", ""),
            "memories": getattr(state, "memories", []),
        }


# 便捷函数
def create_pathology_middleware(config_path: str = None) -> PluggablePathologyMiddleware:
    """创建病理中间件"""
    return PluggablePathologyMiddleware(config_path)
