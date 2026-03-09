"""
外部适配器模块

包含:
- Obsidian适配器
- FlowUs适配器
- 统一记忆网关
"""

from .obsidian_adapter import (
    ObsidianAdapter,
    ObsidianNote,
    LimbicMetadata,
)

from .flowus_adapter import (
    FlowUsAdapter,
    FlowUsPage,
    FlowUsConfig,
    UnifiedMemoryGateway,
)

__all__ = [
    "ObsidianAdapter",
    "ObsidianNote", 
    "LimbicMetadata",
    "FlowUsAdapter",
    "FlowUsPage",
    "FlowUsConfig",
    "UnifiedMemoryGateway",
]
