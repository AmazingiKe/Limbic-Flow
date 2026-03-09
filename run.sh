#!/bin/bash
# 自动部署脚本

echo "开始部署 Limbic-Flow..."

# 检查依赖
echo "检查依赖..."
python -m pip install -r requirements.txt

# 运行测试
echo "运行测试..."
python -m pytest test/

# 格式化代码
echo "格式化代码..."
python format_code.py

# 启动服务
echo "启动服务..."
uvicorn limbic_flow.api.main:app --host 0.0.0.0 --port 8001 --reload
