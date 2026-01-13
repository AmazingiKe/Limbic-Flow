#!/usr/bin/env python3
"""
Limbic-Flow CLI 对话工具

功能：
- 使用完整的 Limbic-Flow 管道进行对话
- 集成情绪引擎，根据输入调整情绪状态
- 自动记录情绪状态到数据库
- 支持多轮对话
- 显示情绪状态变化
- 支持退出命令

使用方法：
1. 确保已配置 .env 文件中的 DEEPSEEK_API_KEY
2. 运行：python limbic_cli.py
3. 输入问题进行对话
4. 输入 'exit' 或 'quit' 退出
"""

import os
import sys
import time
from dotenv import load_dotenv
from limbic_flow.pipeline import LimbicFlowPipeline

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

def format_emotional_state(state):
    """格式化情绪状态输出"""
    pleasure = state["pleasure"]
    arousal = state["arousal"]
    dominance = state["dominance"]
    dopamine = state["dopamine"]
    cortisol = state["cortisol"]
    
    # 情绪描述
    emotion_desc = []
    if pleasure > 0.3:
        emotion_desc.append("开心")
    elif pleasure < -0.3:
        emotion_desc.append("沮丧")
    
    if arousal > 0.3:
        emotion_desc.append("兴奋")
    elif arousal < -0.3:
        emotion_desc.append("平静")
    
    if dominance > 0.3:
        emotion_desc.append("自信")
    elif dominance < -0.3:
        emotion_desc.append("犹豫")
    
    emotion_str = "，".join(emotion_desc) if emotion_desc else "中性"
    
    return f"""
💭 情绪状态: {emotion_str}
   - 愉悦度: {pleasure:.2f}
   - 唤醒度: {arousal:.2f}
   - 控制度: {dominance:.2f}
   - 多巴胺: {dopamine:.2f}
   - 皮质醇: {cortisol:.2f}
"""

def main():
    """主函数"""
    print("=" * 70)
    print("Limbic-Flow CLI 对话工具")
    print("=" * 70)
    print("功能: 集成情绪引擎的智能对话系统")
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
                # 处理输入
                start_time = time.time()
                result = pipeline.process_input(user_input)
                end_time = time.time()
                
                # 打印响应
                print(result["response"])
                print()
                
                # 打印情绪状态
                print(format_emotional_state(result["emotional_state"]))
                
                # 打印处理时间
                print(f"⏱️  处理时间: {end_time - start_time:.2f} 秒")
                print("-" * 70)
                
                # 添加助手回复到历史
                conversation_history.append({"role": "assistant", "content": result["response"]})
                    
            except Exception as e:
                print(f"\n❌ 错误: {str(e)}")
                print("请检查网络连接或 API Key 是否正确")
                print("-" * 70)
                print()
                
    except KeyboardInterrupt:
        print("\n\n再见！")
        sys.exit(0)

if __name__ == "__main__":
    main()