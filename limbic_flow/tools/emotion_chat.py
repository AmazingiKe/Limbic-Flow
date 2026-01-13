#!/usr/bin/env python3
"""
感情对话工具 (Emotion Chat Tool)
"""

import os
import sys

# 添加项目根目录到 Python 路径，确保能找到 limbic_flow 模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import time
from dotenv import load_dotenv
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.core.articulation import MotorCortex, create_articulation_executor
from limbic_flow.core.emotion_engine import EmotionEngine


def load_config():
    """加载配置"""
    load_dotenv()
    
    # 检查必要的环境变量
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: 未配置 DEEPSEEK_API_KEY 环境变量")
        print("请在 .env 文件中设置 DEEPSEEK_API_KEY=your_api_key")
        sys.exit(1)
    
    return {
        "llm_provider": os.getenv("DEFAULT_LLM_PROVIDER", "deepseek"),
        "api_key": api_key
    }


def create_pipeline(config):
    """创建 Limbic-Flow 管道"""
    try:
        pipeline = LimbicFlowPipeline(llm_provider=config["llm_provider"])
        return pipeline
    except Exception as e:
        print(f"❌ 管道初始化失败: {str(e)}")
        sys.exit(1)


class EmotionChatTool:
    """感情对话工具"""
    
    def __init__(self):
        # 加载配置
        self.config = load_config()
        
        # 创建管道
        self.pipeline = create_pipeline(self.config)
        
        # 创建情绪引擎和运动皮层（调整分段策略）
        self.emotion_engine = EmotionEngine()
        self.motor = MotorCortex(
            base_wpm=70,
            min_segment_length=10,  # 增加最小分段长度，避免过度切分
            max_segment_length=50,   # 增加最大分段长度，保持句子完整
            hesitation_base=0.3      # 减少犹豫时间，使对话更流畅
        )
        
        # 对话历史
        self.conversation_history = []
    
    def _get_current_pad_state(self):
        """获取当前 PAD 情绪状态"""
        emotion_state = self.emotion_engine.get_state()
        return {
            "pleasure": emotion_state["pleasure"],
            "arousal": emotion_state["arousal"],
            "dominance": emotion_state["dominance"]
        }
    
    def _analyze_user_emotion(self, user_input):
        """分析用户输入的情绪"""
        user_input_lower = user_input.lower()
        
        pleasure_change = 0.0
        arousal_change = 0.0
        dominance_change = 0.0
        
        # 简单的关键词匹配
        positive_words = ["开心", "高兴", "好", "棒", "happy", "good", "great"]
        negative_words = ["累", "难过", "不好", "烦", "tired", "sad", "bad", "annoyed"]
        urgent_words = ["急", "快", "马上", "urgent", "quick", "immediately"]
        hesitant_words = ["可能", "也许", "不确定", "maybe", "perhaps", "uncertain"]
        
        for word in positive_words:
            if word in user_input_lower:
                pleasure_change += 0.2
                arousal_change += 0.1
        
        for word in negative_words:
            if word in user_input_lower:
                pleasure_change -= 0.2
                arousal_change += 0.1
        
        for word in urgent_words:
            if word in user_input_lower:
                arousal_change += 0.3
        
        for word in hesitant_words:
            if word in user_input_lower:
                dominance_change -= 0.2
        
        # 限制变化范围
        pleasure_change = max(-0.5, min(0.5, pleasure_change))
        arousal_change = max(-0.5, min(0.5, arousal_change))
        dominance_change = max(-0.5, min(0.5, dominance_change))
        
        return pleasure_change, arousal_change, dominance_change
    
    def _action_callback(self, action):
        """动作回调函数"""
        action_type = action.action_type.value
        
        if action_type == "message":
            # 确保句子完整，按句尾标点换行
            content = action.content.strip()
            if content:
                print(content)
    
    def process_input(self, user_input):
        """处理用户输入"""
        # 添加到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 分析用户情绪
        pleasure_change, arousal_change, dominance_change = self._analyze_user_emotion(user_input)
        
        # 更新情绪引擎
        self.emotion_engine.update(
            input_pleasure=pleasure_change,
            input_arousal=arousal_change,
            input_dominance=dominance_change
        )
        
        # 处理输入，获取完整回复
        try:
            result = self.pipeline.process_input(
                user_input,
                streaming=False
            )
            full_response = result["response"]
            
            # 获取当前情绪状态
            pad_state = self._get_current_pad_state()
            
            # 使用运动皮层生成动作流
            actions = self.motor.articulate(full_response, pad_state)
            
            # 执行动作流（只显示消息内容）
            executor = create_articulation_executor(
                action_callback=self._action_callback,
                enable_timing=True,
                enable_logging=False
            )
            
            executor.execute(actions)
            
            # 添加空行分隔
            print()
            
            # 添加助手回复到历史
            self.conversation_history.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
            print("请检查网络连接或 API Key 是否正确")
            print()
    
    def run(self):
        """运行对话循环"""
        try:
            while True:
                # 获取用户输入（不显示提示）
                user_input = input().strip()
                
                # 检查退出命令
                if user_input.lower() in ["exit", "quit", "退出", "退出()"]:
                    print("再见！")
                    break
                
                # 跳过空输入
                if not user_input:
                    continue
                
                # 处理输入
                self.process_input(user_input)
                
        except KeyboardInterrupt:
            print("\n再见！")
            sys.exit(0)


def main():
    """主函数"""
    chat_tool = EmotionChatTool()
    chat_tool.run()


if __name__ == "__main__":
    main()
