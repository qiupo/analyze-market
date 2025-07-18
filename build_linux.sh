#!/bin/bash

echo "🚀 开始构建Linux可执行文件..."

# 清理之前的构建
rm -rf build dist

# 使用PyInstaller构建Linux版本
pyinstaller \
    --onefile \
    --name BandMasterPro-Linux \
    --add-data "src:src" \
    --hidden-import streamlit \
    --hidden-import akshare \
    --hidden-import pandas \
    --hidden-import numpy \
    --hidden-import plotly \
    --hidden-import talib \
    --hidden-import requests \
    --hidden-import python-dateutil \
    --hidden-import colorama \
    main.py

echo "✅ 构建完成！"
echo "📁 可执行文件位置: dist/BandMasterPro-Linux"
echo "📋 使用方法: ./dist/BandMasterPro-Linux" 