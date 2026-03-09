"""
命令系统
"""

from typing import Callable, Dict, List, Optional
import re


class Command:
    """命令"""
    
    def __init__(self, name: str, func: Callable, help: str = ""):
        self.name = name
        self.func = func
        self.help = help


class CommandManager:
    """命令管理器"""
    
    def __init__(self, prefix: str = "/"):
        self.prefix = prefix
        self.commands: Dict[str, Command] = {}
    
    def register(self, name: str, help: str = ""):
        """装饰器注册命令"""
        def decorator(func: Callable):
            self.commands[name] = Command(name, func, help)
            return func
        return decorator
    
    def execute(self, text: str) -> Optional[str]:
        """执行命令"""
        if not text.startswith(self.prefix):
            return None
        
        parts = text[1:].split()
        if not parts:
            return None
        
        name = parts[0]
        args = parts[1:]
        
        if name in self.commands:
            return self.commands[name].func(*args)
        
        return f"未知命令: /{name}"
    
    def get_help(self) -> str:
        """获取帮助"""
        lines = ["可用命令:"]
        for cmd in self.commands.values():
            lines.append(f"  /{cmd.name} - {cmd.help}")
        return "\n".join(lines)


# 全局命令管理器
cmds = CommandManager()


# 示例命令
@cmds.register("help", "显示帮助")
def cmd_help():
    return cmds.get_help()


@cmds.register("status", "显示状态")
def cmd_status():
    return "系统正常"


@cmds.register("version", "显示版本")
def cmd_version():
    return "v0.5.0"
