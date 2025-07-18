#!/bin/bash

echo "🚀 BandMaster Pro - 智策波段交易助手"
echo "=================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

# 检查是否在项目目录中
if [ ! -f "src/app.py" ]; then
    echo "❌ 错误: 未找到 src/app.py 文件"
    echo "请确保在项目根目录中运行此脚本"
    exit 1
fi

echo "✅ 环境检查通过"
echo

# 检查虚拟环境
if [ -d "venv" ]; then
    echo "🔧 激活虚拟环境..."
    source venv/bin/activate
fi

# 检查依赖是否安装
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 安装依赖..."
    pip install -r requirements.txt
fi

echo "🚀 启动应用..."
python3 run.py 