"""
快速启动脚本
"""

import subprocess
import sys
import os


def install():
    """安装依赖"""
    print("安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def test():
    """运行测试"""
    print("运行测试...")
    subprocess.run([sys.executable, "-m", "pytest", "test/", "-v"])


def serve():
    """启动服务"""
    print("启动 API 服务...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "limbic_flow.api.main:app",
        "--host", "0.0.0.0",
        "--port", "8001",
        "--reload"
    ])


def web():
    """启动 Web"""
    print("启动 Web...")
    os.chdir("web")
    subprocess.run([sys.executable, "-m", "http.server", "8080"])


def main():
    if len(sys.argv) < 2:
        print("用法: python run.py [install|test|serve|web]")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "install":
        install()
    elif cmd == "test":
        test()
    elif cmd == "serve":
        serve()
    elif cmd == "web":
        web()
    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
