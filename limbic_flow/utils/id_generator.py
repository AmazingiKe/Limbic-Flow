"""
生成唯一 ID
"""

import uuid
import random
import string
import time


def generate_id(prefix: str = "") -> str:
    """生成唯一 ID"""
    timestamp = str(time.time()).replace(".", "")
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}{timestamp}{random_str}"


def generate_uuid() -> str:
    """生成 UUID"""
    return str(uuid.uuid4())


def generate_short_id(length: int = 8) -> str:
    """生成短 ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_user_id() -> str:
    """生成用户 ID"""
    return f"user_{generate_short_id(12)}"


def generate_session_id() -> str:
    """生成会话 ID"""
    return f"session_{generate_short_id(16)}"


def generate_message_id() -> str:
    """生成消息 ID"""
    return f"msg_{generate_short_id(10)}"
