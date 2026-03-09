"""
安全工具
"""

import hashlib
import hmac
import secrets
from typing import Optional


def generate_token(length: int = 32) -> str:
    """生成安全随机令牌"""
    return secrets.token_urlsafe(length)


def hash_password(password: str, salt: Optional[str] = None) -> tuple:
    """哈希密码"""
    if salt is None:
        salt = secrets.token_hex(16)
    
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    
    return hashed.hex(), salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """验证密码"""
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, hashed)


def generate_api_key() -> str:
    """生成 API Key"""
    return f"sk_{secrets.token_urlsafe(32)}"


def hash_text(text: str, algorithm: str = "sha256") -> str:
    """哈希文本"""
    if algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(text.encode()).hexdigest()
    return hashlib.sha256(text.encode()).hexdigest()
