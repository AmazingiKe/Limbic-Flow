#!/usr/bin/env python3
"""
Limbic-Flow 测试脚本
验证核心组件的基本功能
"""

from limbic_flow.pipeline import LimbicFlowPipeline

def test_basic_functionality():
    """
    测试基本功能
    """
    print("测试 Limbic-Flow 基本功能...")
    
    # 初始化管道
    pipeline = LimbicFlowPipeline()
    
    # 测试不同类型的输入
    test_inputs = [
        "我今天感觉很开心！",
        "我现在很伤心。",
        "告诉我关于你自己。",
        "你最喜欢的记忆是什么？"
    ]
    
    for i, input_text in enumerate(test_inputs):
        print(f"\n测试 {i+1}: {input_text}")
        result = pipeline.process_input(input_text)
        
        print(f"回复: {result['response']}")
        print(f"情绪状态 - P: {result['emotional_state']['pleasure']:.2f}, A: {result['emotional_state']['arousal']:.2f}, D: {result['emotional_state']['dominance']:.2f}")
        print(f"多巴胺: {result['emotional_state']['dopamine']:.2f}, 皮质醇: {result['emotional_state']['cortisol']:.2f}")
        print(f"检索到的记忆: {len(result['memories'])}")

if __name__ == "__main__":
    test_basic_functionality()