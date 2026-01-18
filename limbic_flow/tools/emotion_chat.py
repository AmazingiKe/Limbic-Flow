#!/usr/bin/env python3
"""
感情对话工具 (Emotion Chat Tool)
[重构] 哑终端模式 - 仅负责显示，不负责思考
"""

import os
import sys
import time

# 添加项目根目录到 Python 路径，确保能找到 limbic_flow 模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.core.articulation import ActionType


def load_config():
    """加载配置"""
    load_dotenv()
    
    # 检查必要的环境变量
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        # 尝试检查 OPENAI_API_KEY，如果 LLM_PROVIDER 是 openai
        if os.getenv("DEFAULT_LLM_PROVIDER") == "openai" and os.getenv("OPENAI_API_KEY"):
            pass
        else:
            print("警告: 未配置 DEEPSEEK_API_KEY 环境变量 (默认)")
            # 不强制退出，因为可能使用其他 Provider
            # sys.exit(1)
    
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
    """
    [职责] 哑终端 - 仅负责 I/O
    [场景] 接收 Pipeline 的 Action Stream 并执行显示
    """
    
    def __init__(self):
        # 加载配置
        self.config = load_config()
        
        # 创建管道 (中枢神经系统)
        self.pipeline = create_pipeline(self.config)
        
        # 对话历史 (仅用于本地记录)
        self.conversation_history = []
    
    def process_input(self, user_input):
        """处理用户输入"""
        # 添加到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # 直接消耗 Pipeline 的动作流
            # 这里的 Pipeline 已经是“生物体”，包含了感知、思考和表达
            action_stream = self.pipeline.process_input_stream(user_input)
            
            full_response = ""
            
            # 这里的 action_stream 是一个生成器，会随着 pipeline 内部的处理逐步产生
            # 注意：目前 Brain 的处理是同步的，所以第一个 action 会在 Brain 生成完之后才 yield
            for action in action_stream:
                # 执行动作
                content = self._execute_action(action)
                if content:
                    full_response += content
            
            # 本轮结束
            print() 
            self.conversation_history.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()
            print("请检查网络连接或 API Key 是否正确")
            print()
            
    def _execute_action(self, action):
        """
        执行单个动作
        返回: 如果是消息动作，返回内容；否则返回 None
        """
        if action.action_type == ActionType.TYPING:
            # 模拟“正在输入...”
            duration = action.duration
            # 使用 \r 覆盖当前行
            print(f"\r⌨️  阿皓正在输入... ({duration:.1f}s)", end="", flush=True)
            time.sleep(duration)
            # 清除提示
            print(f"\r{' ' * 40}\r", end="", flush=True)
            return None
            
        elif action.action_type == ActionType.WAIT:
            # 犹豫/停顿
            time.sleep(action.duration)
            return None
            
        elif action.action_type == ActionType.MESSAGE:
            # 发送消息
            content = action.content
            # 打印消息 (阿皓: xxx)
            print(f"阿皓: {content}")
            return content
            
        return None

    def run(self):
        """运行对话循环"""
        print("\n=== Limbic-Flow 原生具身化终端 ===")
        print("输入 'exit' 或 'quit' 退出\n")
        
        try:
            while True:
                # 获取用户输入
                try:
                    user_input = input("你: ").strip()
                except EOFError:
                    break
                
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
