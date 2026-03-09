"""
国际化 (i18n)
"""

from typing import Dict

# 简体中文
zh_CN = {
    "welcome": "欢迎",
    "settings": "设置",
    "emotion": "情绪",
    "save": "保存",
    "cancel": "取消",
    "reset": "重置",
    "loading": "加载中...",
    "error": "错误",
    "success": "成功",
    "send": "发送",
    "input_placeholder": "输入消息...",
    # 情绪
    "pleasure": "愉悦",
    "arousal": "唤醒",
    "dominance": "控制",
    "dopamine": "多巴胺",
    "cortisol": "皮质醇",
    # 模式
    "normal": "正常",
    "depression": "抑郁",
    "alzheimer": "阿尔茨海默",
    "ptsd": "PTSD",
    "hsp": "高敏感",
    # 人格
    "personality_default": "默认",
    "personality_gentle": "温柔",
    "personality_playful": "活泼",
    "personality_wise": "智慧",
    "personality_energetic": "活力",
}

# English
en = {
    "welcome": "Welcome",
    "settings": "Settings",
    "emotion": "Emotion",
    "save": "Save",
    "cancel": "Cancel",
    "reset": "Reset",
    "loading": "Loading...",
    "error": "Error",
    "success": "Success",
    "send": "Send",
    "input_placeholder": "Type a message...",
    "pleasure": "Pleasure",
    "arousal": "Arousal",
    "dominance": "Dominance",
    "dopamine": "Dopamine",
    "cortisol": "Cortisol",
    "normal": "Normal",
    "depression": "Depression",
    "alzheimer": "Alzheimer",
    "ptsd": "PTSD",
    "hsp": "HSP",
}


def get_text(key: str, lang: str = "zh-CN") -> str:
    """获取翻译文本"""
    translations = {"zh-CN": zh_CN, "en": en}
    return translations.get(lang, en).get(key, key)


class I18n:
    """国际化器"""
    
    def __init__(self, lang: str = "zh-CN"):
        self.lang = lang
        self.translations = {"zh-CN": zh_CN, "en": en}
    
    def t(self, key: str) -> str:
        return self.translations.get(self.lang, en).get(key, key)
    
    def set_lang(self, lang: str):
        self.lang = lang
