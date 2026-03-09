"""
情绪配置模块 - 集中管理所有可调整的参数

这个文件类似于人的"性格参数"：
- 每个人的情绪反应速度不同（半衰期）
- 对压力的敏感度不同（阈值）
- 基线情绪状态不同（默认值）
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HalfLifeConfig:
    """
    半衰期配置 - 控制情绪衰减速度
    
    类似于人的"情绪记忆":
    - 有些人很快忘记不愉快的事情（短半衰期）
    - 有些人记得很久（长半衰期）
    """
    pleasure: float = 3600      # 愉悦感衰减周期（秒）
    arousal: float = 1800       # 唤醒度衰减周期
    dominance: float = 2700    # 控制感衰减周期
    dopamine: float = 300      # 多巴胺衰减周期
    cortisol: float = 600      # 皮质醇衰减周期


@dataclass
class BaselineConfig:
    """
    基线配置 - 人的"日常情绪状态"
    
    大多数人有一个默认的情绪基线，而不是完全中性
    """
    pleasure: float = 0.0
    arousal: float = 0.0
    dominance: float = 0.0
    dopamine: float = 0.5      # 正常水平
    cortisol: float = 0.3     # 正常水平


@dataclass
class ThresholdConfig:
    """
    阈值配置 - 触发情绪反应的"敏感度"
    
    类似于人的"脾气":
    - 高敏感的人阈值低，容易被触发
    - 迟钝的人阈值高，不容易受影响
    """
    # 压力触发阈值
    stress_arousal: float = 0.3
    stress_dominance: float = -0.2
    
    # 奖励触发阈值
    reward_pleasure: float = 0.3
    reward_dominance: float = 0.3
    
    # 累积压力参数
    stress_window: int = 5           # 考虑最近N次情绪记录
    stress_history_threshold: float = 0.2  # 历史唤醒度阈值
    stress_history_pleasure: float = -0.2  # 历史愉悦度阈值


@dataclass
class LimbicConfig:
    """
    完整的情绪系统配置
    
    将所有子配置组合在一起，方便统一传递
    """
    half_life: HalfLifeConfig = field(default_factory=HalfLifeConfig)
    baseline: BaselineConfig = field(default_factory=BaselineConfig)
    threshold: ThresholdConfig = field(default_factory=ThresholdConfig)
    
    # 数据库配置
    database_path: str = "amygdala.db"
    
    # 创建默认配置
    @staticmethod
    def relaxed() -> "LimbicConfig":
        """创建放松型配置（情绪稳定，衰减慢）"""
        config = LimbicConfig()
        config.half_life.pleasure = 7200      # 2小时
        config.half_life.arousal = 3600       # 1小时
        config.half_life.dominance = 5400     # 1.5小时
        config.half_life.dopamine = 600       # 10分钟
        config.half_life.cortisol = 1200      # 20分钟
        return config
    
    @staticmethod
    def sensitive() -> "LimbicConfig":
        """创建敏感型配置（情绪波动大，衰减快）"""
        config = LimbicConfig()
        config.half_life.pleasure = 1800      # 30分钟
        config.half_life.arousal = 900        # 15分钟
        config.half_life.dominance = 1200     # 20分钟
        config.half_life.dopamine = 120       # 2分钟
        config.half_life.cortisol = 300       # 5分钟
        config.threshold.stress_arousal = 0.2  # 更敏感
        config.threshold.stress_history_threshold = 0.1
        return config


# 全局默认配置
default_config = LimbicConfig()
