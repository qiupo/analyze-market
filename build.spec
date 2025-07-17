# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 项目根目录
project_root = Path('.').absolute()

# 获取Python环境中streamlit的路径
import streamlit
streamlit_path = Path(streamlit.__file__).parent

a = Analysis(
    ['app.py'],  # 主入口文件
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # 包含项目的Python模块
        ('data_fetcher.py', '.'),
        ('technical_analysis.py', '.'),
        ('visualization.py', '.'), 
        ('config.py', '.'),
        # 包含Streamlit的静态文件
        (str(streamlit_path / 'static'), 'streamlit/static'),
        (str(streamlit_path / 'runtime'), 'streamlit/runtime'),
    ],
    hiddenimports=[
        # 核心依赖
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state',
        'streamlit.runtime.caching',
        'streamlit.components.v1',
        # 数据相关
        'akshare',
        'pandas',
        'numpy',
        'plotly',
        'plotly.graph_objects',
        'plotly.express', 
        'plotly.subplots',
        'requests',
        'talib',
        # 系统模块
        'datetime',
        'json',
        'hashlib',
        'base64',
        'urllib.request',
        'urllib.parse',
        'ssl',
        'certifi',
        'socket',
        'webbrowser',
        'subprocess',
        'time',
        'warnings',
        'colorama',
        # 自定义模块
        'data_fetcher',
        'technical_analysis',
        'visualization',
        'config'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter', 
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'test',
        'unittest',
        'doctest'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BandMasterPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 保留控制台以显示启动信息
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
) 