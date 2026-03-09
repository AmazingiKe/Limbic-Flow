"""
病理中间件 - 记忆扭曲模块

[职责] 在记忆检索后、LLM思考前，根据当前情绪状态扭曲记忆

新版插件化:
- pluggable.py: 从 config/pathology.json 加载规则
- classic.py: 兼容旧版硬编码实现

主要病理类型:
- 抑郁 (Depression): 屏蔽快乐记忆，压低愉悦度
- 阿尔茨海默 (Alzheimer): 高斯噪声 + 阻断近期记忆  
- 创伤后应激 (PTSD): 触发词强制检索创伤记忆
- 高敏感 (HSP): 低阈值放大情绪反应
"""

# 插件化新版
from limbic_flow.middleware.pathology.pluggable import (
    PluggablePathologyMiddleware,
    create_pathology_middleware as create_pluggable_middleware
)

# 兼容旧版
from limbic_flow.middleware.pathology.classic import (
    BasePathologyMiddleware,
    Pathology,
    DepressionPathology,
    AlzheimerPathology,
    PTSDPathology,
    HSPPathology,
    create_pathology_middleware as create_classic_middleware
)

__all__ = [
    # 插件化新版
    "PluggablePathologyMiddleware",
    "create_pluggable_middleware",
    # 兼容旧版
    "BasePathologyMiddleware",
    "Pathology",
    "DepressionPathology",
    "AlzheimerPathology", 
    "PTSDPathology",
    "HSPPathology",
    "create_classic_middleware",
]
