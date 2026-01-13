#!/usr/bin/env python3
"""
测试 Amygdala 模块，生成数据库文件

功能：
- 直接初始化 Amygdala 类
- 触发数据库文件创建
- 测试数据库读写功能
- 验证数据库文件是否生成

使用方法：
1. 运行：python test_amygdala.py
2. 观察是否生成 amygdala.db 文件
3. 检查数据库中的状态记录
"""

import os
import sys
from limbic_flow.core.amygdala import Amygdala

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
    print("测试 Amygdala 模块")
    print("=" * 60)
    print("目标: 初始化 Amygdala 并生成数据库文件")
    print("=" * 60)
    print()
    
    # 检查初始状态
    print("=== 初始状态检查 ===")
    db_exists_before = check_db_file()
    
    # 初始化 Amygdala
    print("\n=== 初始化 Amygdala ===")
    try:
        amygdala = Amygdala()
        print("✅ Amygdala 初始化成功")
        print(f"数据库路径: {amygdala.db_path}")
        
        # 检查是否生成数据库文件
        print("\n=== 初始化后检查 ===")
        db_exists_after = check_db_file()
        
        # 记录情绪状态
        print("\n=== 测试数据库写入 ===")
        test_state = {
            "pleasure": 0.5,
            "arousal": 0.3,
            "dominance": 0.2,
            "dopamine": 0.7,
            "cortisol": 0.2
        }
        
        amygdala.log_state(test_state, context={"test": "initial state"})
        print("✅ 情绪状态记录成功")
        
        # 读取情绪状态
        print("\n=== 测试数据库读取 ===")
        history = amygdala.get_state_history()
        print(f"✅ 读取到 {len(history)} 条记录")
        
        if history:
            latest = history[0]
            print(f"最新记录: {latest}")
        
        # 再次检查数据库
        print("\n=== 最终检查 ===")
        db_exists_final = check_db_file()
        
        # 总结
        print("\n=== 测试总结 ===")
        print(f"数据库创建: {'✅ 成功' if (not db_exists_before and db_exists_final) else '❌ 失败'}")
        print(f"数据库写入: {'✅ 成功' if len(history) > 0 else '❌ 失败'}")
        print(f"数据库读取: {'✅ 成功' if len(history) > 0 else '❌ 失败'}")
        
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