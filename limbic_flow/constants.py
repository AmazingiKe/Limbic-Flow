"""
常量定义
"""

# 版本
VERSION = "0.5.0"
VERSION_NAME = "Emotional Flow"

# API
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# 默认配置
DEFAULT_CONFIG = {
    "llm_provider": "mock",
    "emotion_model": "occ",
    "personality": "default",
    "pathology": "none",
    "memory_enabled": True,
}

# LLM 提供商
LLM_PROVIDERS = [
    "mock",
    "openai",
    "deepseek",
    "anthropic",
    "ollama",
    "google",
    "cohere",
]

# 情感模型
EMOTION_MODELS = [
    "occ",  # OCC 认知情绪模型
    "pad",  # PAD 维度情绪模型
]

# 人格类型
PERSONALITIES = [
    "default",
    "gentle",
    "playful",
    "wise",
    "energetic",
    "sarcastic",
    "mysterious",
]

# 病理类型
PATHOLOGIES = [
    "none",
    "depression",
    "alzheimer",
    "ptsd",
    "hsp",
    "anxiety",
]

# OCC 情绪类型
OCC_EMOTIONS = [
    "joy", "sadness", "anger", "fear",
    "surprise", "disgust", "hope", "relief",
    "satisfaction", "disappointment", "pride", "shame",
    "admiration", "reproach", "love", "hate",
    "gratitude", "distress", "happiness", "sadness",
]

# 事件类型
EVENT_TYPES = [
    "user_message",
    "bot_response",
    "emotion_changed",
    "memory_stored",
    "error",
]

# 文件大小限制
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB

# 时间常量
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY

# 情绪半衰期默认值
DEFAULT_HALF_LIFE = {
    "pleasure": 3600,      # 1小时
    "arousal": 1800,       # 30分钟
    "dominance": 2700,      # 45分钟
    "dopamine": 300,       # 5分钟
    "cortisol": 600,       # 10分钟
}

# 错误码
ERROR_CODES = {
    1000: "未知错误",
    1001: "无效的请求",
    1002: "认证失败",
    1003: "权限不足",
    1004: "资源不存在",
    1005: "请求过于频繁",
    1006: "服务不可用",
    1007: "LLM 调用失败",
    1008: "无效的配置",
}

# HTTP 状态码
HTTP_STATUS = {
    200: "OK",
    201: "Created",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    429: "Too Many Requests",
    500: "Internal Server Error",
    503: "Service Unavailable",
}
