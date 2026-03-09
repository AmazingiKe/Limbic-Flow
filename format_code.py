"""
自动代码格式化
"""

import subprocess
import sys


def format_code():
    """格式化代码"""
    print("格式化 Python 代码...")
    
    # 使用 black
    try:
        subprocess.run([sys.executable, '-m', 'black', 'limbic_flow/', 'config/', 'test/'])
        print("✓ Black 格式化完成")
    except Exception as e:
        print(f"✗ Black 失败: {e}")
    
    # 使用 isort
    try:
        subprocess.run([sys.executable, '-m', 'isort', 'limbic_flow/', 'config/', 'test/'])
        print("✓ isort 排序完成")
    except Exception as e:
        print(f"✗ isort 失败: {e}")
    
    # 使用 flake8 检查
    try:
        subprocess.run([sys.executable, '-m', 'flake8', 'limbic_flow/', '--max-line-length=100'])
        print("✓ flake8 检查完成")
    except Exception as e:
        print(f"✗ flake8 检查失败: {e}")


def lint_code():
    """代码检查"""
    print("运行代码检查...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pylint', 'limbic_flow/'])
    except Exception as e:
        print(f"✗ pylint 失败: {e}")


if __name__ == '__main__':
    format_code()
