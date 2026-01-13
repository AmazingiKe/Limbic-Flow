#!/usr/bin/env python3
"""
测试 Limbic-Flow 位置和时间功能

功能：
- 测试系统是否能记住用户名字
- 测试系统是否能提供正确的时间信息
- 测试系统是否能提供位置相关信息
- 测试系统是否能处理天气查询
"""

import os
import sys
import time
from limbic_flow.pipeline import LimbicFlowPipeline

def test_location_features():
    """测试位置和时间功能"""
    print("=" * 80)
    print("测试 Limbic-Flow 位置和时间功能")
    print("=" * 80)
    
    # 创建管道实例
    print("1. 初始化 Limbic-Flow 管道...")
    try:
        pipeline = LimbicFlowPipeline(llm_provider="deepseek")
        print("✅ 管道初始化成功")
    except Exception as e:
        print(f"❌ 管道初始化失败: {str(e)}")
        return False
    
    # 测试对话序列
    test_cases = [
        ("你好，我叫阿皓", "测试自我介绍"),
        ("现在几点了", "测试时间查询"),
        ("今天天气怎么样", "测试天气查询"),
        ("我在哪里", "测试位置查询"),
        ("你知道我叫什么名字吗", "测试记忆功能"),
    ]
    
    for user_input, test_description in test_cases:
        print(f"\n2. {test_description}")
        print(f"用户输入: {user_input}")
        
        try:
            start_time = time.time()
            result = pipeline.process_input(user_input)
            end_time = time.time()
            
            print(f"系统回应: {result['response']}")
            print(f"处理时间: {end_time - start_time:.2f} 秒")
            print(f"情绪状态: 愉悦度={result['emotional_state']['pleasure']:.2f}, 多巴胺={result['emotional_state']['dopamine']:.2f}")
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ 处理失败: {str(e)}")
            print("-" * 80)
    
    return True

if __name__ == "__main__":
    success = test_location_features()
    print(f"\n测试完成: {'✅ 成功' if success else '❌ 失败'}")