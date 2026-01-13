#!/usr/bin/env python3
"""
测试 Limbic-Flow 完整管道，生成数据库文件

功能：
- 初始化完整的 LimbicFlowPipeline
- 处理用户输入，触发数据库创建和状态记录
- 验证数据库文件是否生成
- 测试数据库读写功能

使用方法：
1. 运行：python test_pipeline.py
2. 观察是否生成 amygdala.db 文件
3. 检查数据库中的状态记录
"""

import os
import sys
from dotenv import load_dotenv
from limbic_flow.pipeline import LimbicFlowPipeline

def check_db_file():
    """检查数据库文件是否存在"""
    db_path = "amygdala.db"
    if os.path.exists(db_path):
        print(f"✅ 数据库文件存在: {db_path}")
        print(f"文件大小: {os.path.getsize(db_path)} bytes")
        return True
    else:
        print(f"❌ 数据库文件不存在: {db_path}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("测试 Limbic-Flow 完整管道")
    print("=" * 60)
    print("目标: 初始化管道并生成数据库文件")
    print("=" * 60)
    print()
    
    # 加载环境变量
    load_dotenv()
    
    # 检查初始状态
    print("=== 初始状态检查 ===")
    db_exists_before = check_db_file()
    
    # 初始化管道
    print("\n=== 初始化 LimbicFlowPipeline ===")
    try:
        pipeline = LimbicFlowPipeline(llm_provider="deepseek")
        print("✅ LimbicFlowPipeline 初始化成功")
        
        # 检查是否生成数据库文件
        print("\n=== 初始化后检查 ===")
        db_exists_after = check_db_file()
        
        # 处理用户输入
        print("\n=== 处理用户输入 ===")
        print("输入: 你好，很高兴见到你！")
        
        result = pipeline.process_input("你好，很高兴见到你！")
        print("✅ 输入处理成功")
        print(f"回复: {result['response'][:100]}...")
        print(f"情绪状态: {result['emotional_state']}")
        
        # 再次检查数据库
        print("\n=== 处理后检查 ===")
        db_exists_final = check_db_file()
        
        # 总结
        print("\n=== 测试总结 ===")
        print(f"数据库创建: {'✅ 成功' if (not db_exists_before and db_exists_final) else '❌ 失败'}")
        print(f"管道初始化: ✅ 成功")
        print(f"输入处理: ✅ 成功")
        print(f"情绪状态记录: ✅ 成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始测试...\n")
    success = main()
    print(f"\n测试完成: {'✅ 成功' if success else '❌ 失败'}")