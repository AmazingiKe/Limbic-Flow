#!/usr/bin/env python3
"""
Limbic-Flow 流式对话工具

功能：
- 使用完整的 Limbic-Flow 管道进行对话
- 集成情绪引擎，根据输入调整情绪状态
- 支持多轮对话
- 支持流式输出，分段显示回复
- 支持退出命令

使用方法：
1. 确保已配置 .env 文件中的 DEEPSEEK_API_KEY
2. 运行：python cli_chat.py
3. 输入问题进行对话
4. 输入 'exit' 或 'quit' 退出
"""

import os
import sys
import time
from dotenv import load_dotenv
from limbic_flow.pipeline import LimbicFlowPipeline
from limbic_flow.core.streaming import StreamingManager, ConsoleStreamingOutput


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
        print("✅ Limbic-Flow 管道初始化成功")
        print(f"🌐 LLM 提供商: {config['llm_provider']}")
        print()
        return pipeline
    except Exception as e:
        print(f"❌ 管道初始化失败: {str(e)}")
        sys.exit(1)


def main():
    """主函数"""
    print("=" * 70)
    print("Limbic-Flow 流式对话工具")
    print("=" * 70)
    print("功能: 集成情绪引擎的智能对话系统（支持流式输出）")
    print("提示: 输入问题进行对话，输入 'exit' 或 'quit' 退出")
    print("=" * 70)
    print()
    
    # 加载配置
    config = load_config()
    
    # 创建管道
    pipeline = create_pipeline(config)
    
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
            
            # 添加到对话历史
            conversation_history.append({"role": "user", "content": user_input})
            
            # 发送请求
            print("Limbic-Flow: ", end="", flush=True)
            
            try:
                # 创建流式输出管理器
                streaming_output = ConsoleStreamingOutput(chunk_size=30, delay=0.05)
                streaming_manager = StreamingManager(streaming_output)
                
                # 定义流式处理函数
                def stream_generator(callback):
                    # 处理输入，使用流式回调
                    result = pipeline.process_input(
                        user_input,
                        streaming=True,
                        streaming_callback=callback
                    )
                    return result["response"]
                
                # 执行流式处理
                start_time = time.time()
                full_response = streaming_manager.stream(stream_generator)
                end_time = time.time()
                
                print()
                print()
                
                # 添加助手回复到历史
                conversation_history.append({"role": "assistant", "content": full_response})
                    
            except Exception as e:
                print(f"\n\n❌ 错误: {str(e)}")
                print("请检查网络连接或 API Key 是否正确")
                print("-" * 70)
                print()
                
    except KeyboardInterrupt:
        print("\n\n再见！")
        sys.exit(0)


if __name__ == "__main__":
    main()
