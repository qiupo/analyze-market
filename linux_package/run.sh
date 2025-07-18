#!/bin/bash

echo "🚀 BandMaster Pro - 智策波段交易助手"
echo "=================================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import streamlit, akshare, pandas, numpy, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 安装依赖..."
    pip3 install -r requirements.txt
fi

# 启动应用
echo "🌐 启动Web应用..."
python3 main.py 