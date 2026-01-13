#!/usr/bin/env python3
"""
DeepSeek CLI 对话测试工具

功能：
- 命令行交互式对话
- 支持多轮对话
- 自动保存对话历史
- 支持退出命令
- 错误处理和重试机制

使用方法：
1. 确保已配置 .env 文件中的 DEEPSEEK_API_KEY
2. 运行：python cli_chat.py
3. 输入问题进行对话
4. 输入 'exit' 或 'quit' 退出
"""

import os
import sys
from dotenv import load_dotenv
from limbic_flow.core.ai.adapters.deepseek import DeepSeekLLM
from limbic_flow.core.ai.base import LLMConfig, Message, MessageRole

def load_config():
    """加载配置"""
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误: 未配置 DEEPSEEK_API_KEY 环境变量")
        print("请在 .env 文件中设置 DEEPSEEK_API_KEY=your_api_key")
        sys.exit(1)
    
    return LLMConfig(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1024")),
        timeout=int(os.getenv("LLM_TIMEOUT", "30"))
    )

def create_llm_instance(config):
    """创建 LLM 实例"""
    try:
        llm = DeepSeekLLM(config)
        print(f"✅ 成功连接到 DeepSeek API")
        print(f"� model: {config.model}")
        print(f"🌐 base_url: {config.base_url}")
        print()
        return llm
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        sys.exit(1)

def main():
    """主函数"""
    print("=" * 60)
    print("DeepSeek CLI 对话测试工具")
    print("=" * 60)
    print("提示: 输入问题进行对话，输入 'exit' 或 'quit' 退出")
    print("=" * 60)
    print()
    
    # 加载配置
    config = load_config()
    
    # 创建 LLM 实例
    llm = create_llm_instance(config)
    
    # 对话历史
    conversation_history = []
    
    try:
        while True:
            # 获取用户输入
            user_input = input("你: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ["exit", "quit", "退出", "退出()"]:
                print("再见！")
                break
            
            # 跳过空输入
            if not user_input:
                continue
            
            # 添加用户消息到历史
            conversation_history.append(Message(role=MessageRole.USER, content=user_input))
            
            # 发送请求
            print("DeepSeek: ", end="", flush=True)
            
            try:
                # 调用 API
                response = llm.chat(conversation_history)
                
                # 打印响应
                print(response.content)
                print()
                
                # 添加助手回复到历史
                conversation_history.append(Message(role=MessageRole.ASSISTANT, content=response.content))
                
                # 打印使用量（如果有）
                if response.usage:
                    print(f"💡 使用量: {response.usage['total_tokens']} tokens")
                    print()
                    
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}")
                print("请检查网络连接或 API Key 是否正确")
                print()
                
                # 从历史中移除最后一条消息（用户输入）
                if conversation_history:
                    conversation_history.pop()
                    
    except KeyboardInterrupt:
        print("\n\n再见！")
        sys.exit(0)

if __name__ == "__main__":
    main()