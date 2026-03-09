"""
CLI 入口
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Limbic-Flow - 有情绪的 AI 助手"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 运行服务
    serve_parser = subparsers.add_parser("serve", help="启动 API 服务")
    serve_parser.add_argument("--host", default="0.0.0.0", help="主机")
    serve_parser.add_argument("--port", type=int, default=8001, help="端口")
    serve_parser.add_argument("--reload", action="store_true", help="热重载")
    
    # 运行 Web
    serve_parser.add_argument("--web", action="store_true", help="同时启动 Web 页面")
    
    # 测试
    test_parser = subparsers.add_parser("test", help="运行测试")
    test_parser.add_argument("--module", help="指定模块")
    
    # 初始化
    init_parser = subparsers.add_parser("init", help="初始化项目")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        import uvicorn
        from limbic_flow.api.main import app
        
        print(f"🚀 启动服务: http://{args.host}:{args.port}")
        
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.reload
        )
    
    elif args.command == "test":
        import pytest
        sys.exit(pytest.main(["-v", args.module or "test/"]))
    
    elif args.command == "init":
        # 创建必要目录
        dirs = ["config", "logs", "data"]
        for d in dirs:
            Path(d).mkdir(exist_ok=True)
        
        # 创建默认配置
        config_path = Path("config/settings.json")
        if not config_path.exists():
            default_config = {
                "system": {"debug": True},
                "llm": {"provider": "mock"},
                "emotion": {"enabled": True}
            }
            import json
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=2)
        
        print("✅ 初始化完成!")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
