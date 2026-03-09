"""
部署脚本
"""

import os
import sys
import subprocess


def check_requirements():
    """检查依赖"""
    print("检查依赖...")
    
    with open("requirements.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                print(f"  - {line}")


def install():
    """安装"""
    print("安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def deploy_docker():
    """Docker 部署"""
    print("构建 Docker 镜像...")
    subprocess.run(["docker", "build", "-t", "limbic-flow:latest", "."])
    
    print("运行容器...")
    subprocess.run([
        "docker", "run", "-d",
        "-p", "8001:8001",
        "--name", "limbic-flow",
        "limbic-flow:latest"
    ])


def deploy_render():
    """Render 部署"""
    print("部署到 Render...")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="部署脚本")
    parser.add_argument("action", choices=["install", "docker", "render"])
    
    args = parser.parse_args()
    
    if args.action == "install":
        install()
    elif args.action == "docker":
        deploy_docker()
    elif args.action == "render":
        deploy_render()


if __name__ == "__main__":
    main()
