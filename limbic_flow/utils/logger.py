"""
日志工具模块

提供统一的日志记录功能，支持控制台和文件输出
"""

import logging
import os
import sys
from typing import Optional
from pathlib import Path


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True
) -> logging.Logger:
    """
    设置日志记录器
    
    [职责] 创建并配置日志记录器，支持控制台和文件输出
    [场景] 在各个模块中初始化日志系统
    [可替换性] 可通过参数自定义日志行为
    
    Args:
        name: 日志记录器名称，通常使用模块名
        level: 日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）
        log_format: 日志格式字符串
        log_file: 日志文件路径（相对于 logs 目录）
        enable_console: 是否启用控制台输出
        enable_file: 是否启用文件输出
    
    Returns:
        logging.Logger: 配置好的日志记录器实例
    
    Example:
        >>> logger = setup_logger("my_module")
        >>> logger.info("这是一条信息日志")
        >>> logger.error("这是一条错误日志")
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # 设置日志格式
    log_format_str = log_format or os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    formatter = logging.Formatter(log_format_str, datefmt="%Y-%m-%d %H:%M:%S")
    
    # 添加控制台 handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 添加文件 handler
    if enable_file:
        # 确保 logs 目录存在
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # 设置日志文件路径
        file_path = logs_dir / (log_file or f"{name}.log")
        
        # 创建文件 handler
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取或创建日志记录器
    
    [职责] 提供便捷的日志记录器获取方式
    [场景] 在模块中快速获取日志记录器
    [可替换性] 使用默认配置，无需手动设置
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logging.Logger: 日志记录器实例
    
    Example:
        >>> logger = get_logger("my_module")
        >>> logger.info("这是一条信息日志")
    """
    logger = logging.getLogger(name)
    
    # 如果 logger 已经有 handler，直接返回
    if logger.handlers:
        return logger
    
    # 否则使用默认配置创建
    return setup_logger(name)


class LoggerMixin:
    """
    日志混入类
    
    [职责] 为类提供便捷的日志功能
    [场景] 在需要日志功能的类中继承此类
    [可替换性] 可通过覆盖 logger_name 属性自定义日志名称
    
    Example:
        >>> class MyClass(LoggerMixin):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.logger.info("类已初始化")
    """
    
    logger_name: Optional[str] = None
    
    @property
    def logger(self) -> logging.Logger:
        """
        获取日志记录器
        
        Returns:
            logging.Logger: 日志记录器实例
        """
        if self.logger_name is None:
            self.logger_name = self.__class__.__name__
        return get_logger(self.logger_name)


# 创建全局日志记录器
logger = get_logger("limbic_flow")
