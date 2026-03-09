"""
适配器模式
"""

from typing import Any


class OldEmotionAPI:
    """旧API"""
    def get_mood(self):
        return {"mood": "happy"}
    
    def set_mood(self, mood):
        print(f"Setting mood: {mood}")


class NewEmotionSystem:
    """新系统"""
    def get_emotion_state(self):
        return {"emotion": "joy", "intensity": 0.8}
    
    def update_emotion_state(self, state):
        print(f"Updating state: {state}")


class EmotionAdapter:
    """适配器"""
    def __init__(self, old_api: OldEmotionAPI):
        self.old_api = old_api
    
    def get_emotion_state(self):
        mood = self.old_api.get_mood()
        return {"emotion": mood.get("mood"), "intensity": 0.5}
    
    def update_emotion_state(self, state):
        mood = state.get("emotion", "neutral")
        self.old_api.set_mood(mood)


# 使用示例
old = OldEmotionAPI()
adapter = EmotionAdapter(old)
print(adapter.get_emotion_state())
