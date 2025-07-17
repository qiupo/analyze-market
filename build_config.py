#!/usr/bin/env python3
"""
PyInstaller构建配置
"""

import PyInstaller.config
import PyInstaller.building.build_main
import PyInstaller.building.api
import os
import sys

# 隐藏导入配置 - 确保所有必要的模块被包含
hidden_imports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.state',
    'streamlit.runtime.caching',
    'akshare',
    'pandas',
    'numpy',
    'plotly',
    'plotly.graph_objects',
    'plotly.express',
    'plotly.subplots',
    'requests',
    'colorama',
    'talib',
    'datetime',
    'warnings',
    'hashlib',
    'base64',
    'pathlib',
    'socket',
    'webbrowser',
    'subprocess',
    'time',
    'json',
    'urllib',
    'urllib.request',
    'urllib.parse',
    'ssl',
    'certifi',
    # 数据获取相关
    'data_fetcher',
    'technical_analysis', 
    'visualization',
    'config'
]

# 数据文件配置
datas = [
    ('config.py', '.'),
    ('data_fetcher.py', '.'),
    ('technical_analysis.py', '.'),
    ('visualization.py', '.'),
]

# 排除不需要的模块以减小文件大小
excludes = [
    'matplotlib',
    'tkinter',
    'PyQt5',
    'PyQt6',
    'PySide2',
    'PySide6',
    'test',
    'unittest',
    'doctest',
    'argparse',
    'pdb',
    'profile',
    'pstats',
    'sqlite3',
    'bz2',
    'lzma',
    'zipfile',
    'tarfile'
]

# Streamlit特定配置
streamlit_runtime_secrets_toml = []
streamlit_config_toml = []

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__)) 