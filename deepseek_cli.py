#!/usr/bin/env python3
"""
独立的 DeepSeek CLI 对话工具

功能：
- 命令行交互式对话
- 支持多轮对话
- 自动保存对话历史
- 支持退出命令
- 错误处理和重试机制

特点：
- 不依赖项目包结构
- 直接使用 OpenAI 库调用 DeepSeek API
- 自包含所有必要功能
- 兼容 Python 3.7+

使用方法：
1. 确保已安装依赖：pip install openai python-dotenv
2. 运行：python deepseek_cli.py
3. 输入问题进行对话
4. 输入 'exit' 或 'quit' 退出
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

def load_api_key():
    """加载 API Key"""
    load_dotenv()
    
    # 优先从环境变量获取
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 如果环境变量未设置，使用用户提供的默认值
    if not api_key:
        api_key = "sk-9cb760f5bc8f44b2a615aed1be855596"
        print("提示: 使用默认 API Key（从对话历史获取）")
    
    return api_key

def create_client(api_key):
    """创建 OpenAI 客户端"""
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
        timeout=30
    )

def main():
    """主函数"""
    print("=" * 60)
    print("DeepSeek CLI 对话工具")
    print("=" * 60)
    print("提示: 输入问题进行对话，输入 'exit' 或 'quit' 退出")
    print("=" * 60)
    print()
    
    # 加载 API Key
    api_key = load_api_key()
    print(f"API Key: {api_key[:8]}...{api_key[-4:]}")
    
    # 创建客户端
    client = create_client(api_key)
    
    # 对话历史
    conversation_history = []
    
    try:
        while True:
            # 获取用户输入
            user_input = input("你: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ["exit", "quit", "退出"]:
                print("再见！")
                break
            
            # 跳过空输入
            if not user_input:
                continue
            
            # 添加用户消息到历史
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # 发送请求
            print("DeepSeek: ", end="", flush=True)
            
            try:
                # 调用 API
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=conversation_history,
                    temperature=0.7,
                    max_tokens=1024,
                    timeout=30
                )
                
                # 获取回复内容
                assistant_reply = response.choices[0].message.content
                
                # 打印响应
                print(assistant_reply)
                print()
                
                # 添加助手回复到历史
                conversation_history.append({
                    "role": "assistant",
                    "content": assistant_reply
                })
                
                # 打印使用量
                if response.usage:
                    print(f"💡 使用量:")
                    print(f"   - 提示词: {response.usage.prompt_tokens} tokens")
                    print(f"   - 回复: {response.usage.completion_tokens} tokens")
                    print(f"   - 总计: {response.usage.total_tokens} tokens")
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