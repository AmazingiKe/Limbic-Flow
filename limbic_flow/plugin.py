"""
插件系统 - 扩展 Limbic-Flow 功能

参考 AstrBot 插件设计:
- 插件生命周期管理
- 钩子注册
- 配置管理
"""

import importlib
import os
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class PluginMetadata:
    """插件元数据"""
    name: str
    version: str
    author: str = "Unknown"
    description: str = ""
    dependencies: List[str] = field(default_factory=list)


class Plugin:
    """
    插件基类
    
    所有插件必须继承此类
    """
    
    metadata: PluginMetadata
    
    def __init__(self):
        self.enabled = True
        self.config = {}
    
    def on_load(self):
        """插件加载时调用"""
        pass
    
    def on_unload(self):
        """插件卸载时调用"""
        pass
    
    def on_enable(self):
        """启用时调用"""
        pass
    
    def on_disable(self):
        """禁用时调用"""
        pass


class PluginHook:
    """插件钩子"""
    
    def __init__(self, name: str):
        self.name = name
        self.callbacks: List[Callable] = []
    
    def register(self, callback: Callable):
        self.callbacks.append(callback)
    
    def unregister(self, callback: Callable):
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    async def call(self, *args, **kwargs):
        """调用所有注册的回调"""
        for callback in self.callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)


class PluginManager:
    """
    插件管理器
    
    负责插件的加载、卸载、启用、禁用
    """
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, PluginHook] = {}
        self._load_builtins()
    
    def _load_builtins(self):
        """加载内置插件"""
        # 可以在这里加载内置插件
        pass
    
    def register_hook(self, name: str) -> PluginHook:
        """注册钩子"""
        if name not in self.hooks:
            self.hooks[name] = PluginHook(name)
        return self.hooks[name]
    
    def add_hook(self, name: str, callback: Callable):
        """添加钩子回调"""
        if name not in self.hooks:
            self.hooks[name] = PluginHook(name)
        self.hooks[name].register(callback)
    
    async def trigger_hook(self, name: str, *args, **kwargs):
        """触发钩子"""
        if name in self.hooks:
            await self.hooks[name].call(*args, **kwargs)
    
    def load_plugin(self, plugin_class: type, config: Dict = None) -> Plugin:
        """
        加载插件
        
        Args:
            plugin_class: 插件类
            config: 插件配置
        
        Returns:
            加载的插件实例
        """
        # 实例化
        plugin = plugin_class()
        
        if config:
            plugin.config = config
        
        # 存储
        name = plugin.metadata.name
        self.plugins[name] = plugin
        
        # 调用加载钩子
        try:
            plugin.on_load()
            if plugin.enabled:
                plugin.on_enable()
        except Exception as e:
            print(f"Failed to load plugin {name}: {e}")
            del self.plugins[name]
        
        return plugin
    
    def unload_plugin(self, name: str):
        """卸载插件"""
        if name in self.plugins:
            plugin = self.plugins[name]
            try:
                plugin.on_disable()
                plugin.on_unload()
            except Exception as e:
                print(f"Error unloading plugin {name}: {e}")
            del self.plugins[name]
    
    def enable_plugin(self, name: str):
        """启用插件"""
        if name in self.plugins:
            plugin = self.plugins[name]
            if not plugin.enabled:
                plugin.enabled = True
                plugin.on_enable()
    
    def disable_plugin(self, name: str):
        """禁用插件"""
        if name in self.plugins:
            plugin = self.plugins[name]
            if plugin.enabled:
                plugin.enabled = False
                plugin.on_disable()
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """获取插件"""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict]:
        """列出所有插件"""
        return [
            {
                "name": p.metadata.name,
                "version": p.metadata.version,
                "author": p.metadata.author,
                "enabled": p.enabled
            }
            for p in self.plugins.values()
        ]


# 全局插件管理器
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """获取全局插件管理器"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


# 示例插件
class ExamplePlugin(Plugin):
    """示例插件"""
    
    metadata = PluginMetadata(
        name="example",
        version="1.0.0",
        author="Limbic-Flow",
        description="这是一个示例插件"
    )
    
    def on_load(self):
        print(f"插件 {self.metadata.name} 已加载")
        
        # 注册钩子
        manager = get_plugin_manager()
        manager.add_hook("before_response", self.before_response_hook)
    
    async def before_response_hook(self, state):
        """响应前钩子"""
        print("Before response hook triggered")
        return state


import asyncio
