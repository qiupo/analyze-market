#!/usr/bin/env python3
"""
BandMaster Pro 自动化打包脚本
支持Windows、macOS、Linux跨平台打包
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✅ PyInstaller 已安装")
        return True
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("正在安装 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller 安装成功")
            return True
        except Exception as e:
            print(f"❌ PyInstaller 安装失败: {e}")
            return False

def clean_build():
    """清理之前的构建文件"""
    print("🧹 清理构建目录...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除: {dir_name}")

def create_main_entry():
    """创建主入口文件"""
    main_content = '''#!/usr/bin/env python3
"""
BandMaster Pro 主入口文件
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket
from pathlib import Path

def find_available_port(start_port=8501, max_port=8600):
    """查找可用端口"""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return start_port

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 BandMaster Pro - 智策波段交易助手")
    print("=" * 60)
    
    # 获取可用端口
    port = find_available_port()
    
    print(f"📡 启动服务...")
    print(f"🌐 访问地址: http://localhost:{port}")
    print("=" * 60)
    
    # 获取应用文件路径
    if getattr(sys, 'frozen', False):
        # 打包环境
        base_path = sys._MEIPASS
        app_path = os.path.join(base_path, 'app.py')
    else:
        # 开发环境
        app_path = 'app.py'
    
    try:
        # 启动Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ]
        
        print("⏳ 正在启动应用...")
        process = subprocess.Popen(cmd)
        
        # 等待启动
        time.sleep(3)
        
        # 打开浏览器
        webbrowser.open(f'http://localhost:{port}')
        print("✅ 应用已启动")
        print("\\n按 Ctrl+C 停止应用")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\\n🛑 正在停止应用...")
            process.terminate()
            print("✅ 应用已停止")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
'''
    
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)
    print("✅ 主入口文件创建完成")

def build_package():
    """执行打包"""
    print("📦 开始打包...")
    
    # 获取系统信息
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    print(f"🖥️  目标平台: {system} ({arch})")
    
    # 构建命令
    cmd = [
        'pyinstaller',
        '--onefile',  # 打包成单文件
        '--windowed' if system == 'windows' else '--console',  # Windows隐藏控制台
        '--name=BandMasterPro',
        '--distpath=dist',
        '--workpath=build', 
        '--specpath=.',
        '--clean',
        # 添加数据文件
        '--add-data=data_fetcher.py;.',
        '--add-data=technical_analysis.py;.',
        '--add-data=visualization.py;.',
        '--add-data=config.py;.',
        '--add-data=app.py;.',
        # 隐藏导入
        '--hidden-import=streamlit',
        '--hidden-import=akshare',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=plotly',
        '--hidden-import=talib',
        'main.py'
    ]
    
    # Windows特殊处理
    if system == 'windows':
        cmd.extend(['--hidden-import=win32api', '--hidden-import=win32gui'])
    
    try:
        subprocess.check_call(cmd)
        print("✅ 打包成功!")
        
        # 显示输出信息
        dist_path = Path('dist')
        if dist_path.exists():
            files = list(dist_path.glob('*'))
            print(f"📁 输出目录: {dist_path.absolute()}")
            for file in files:
                size = file.stat().st_size / (1024 * 1024)  # MB
                print(f"   📄 {file.name} ({size:.1f} MB)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        return False

def create_launcher_scripts():
    """创建启动脚本"""
    print("📝 创建启动脚本...")
    
    # Windows批处理文件
    batch_content = '''@echo off
title BandMaster Pro - 智策波段交易助手
echo.
echo ========================================
echo   BandMaster Pro - 智策波段交易助手
echo ========================================
echo.
echo 正在启动应用...
echo.

if exist "BandMasterPro.exe" (
    start /wait BandMasterPro.exe
) else (
    echo 错误: 找不到 BandMasterPro.exe
    echo 请确保文件在同一目录下
    pause
)
'''
    
    with open('启动应用.bat', 'w', encoding='gbk') as f:
        f.write(batch_content)
    
    # Shell脚本 (macOS/Linux)
    shell_content = '''#!/bin/bash
echo "========================================"
echo "  BandMaster Pro - 智策波段交易助手"
echo "========================================"
echo
echo "正在启动应用..."
echo

if [ -f "./BandMasterPro" ]; then
    ./BandMasterPro
else
    echo "错误: 找不到 BandMasterPro"
    echo "请确保文件在同一目录下"
    read -p "按回车键退出..."
fi
'''
    
    with open('启动应用.sh', 'w', encoding='utf-8') as f:
        f.write(shell_content)
    
    # 设置执行权限
    if platform.system() != 'Windows':
        os.chmod('启动应用.sh', 0o755)
    
    print("✅ 启动脚本创建完成")

def create_readme():
    """创建说明文档"""
    readme_content = '''# BandMaster Pro - 智策波段交易助手

## 📦 打包版本说明

这是 BandMaster Pro 的独立打包版本，无需安装 Python 环境即可直接运行。

## 🚀 快速启动

### Windows 系统
1. 双击 `启动应用.bat` 或直接运行 `BandMasterPro.exe`
2. 等待应用启动（首次启动可能需要10-30秒）
3. 浏览器会自动打开应用界面

### macOS/Linux 系统  
1. 打开终端，运行 `./启动应用.sh` 或直接运行 `./BandMasterPro`
2. 等待应用启动
3. 浏览器会自动打开应用界面

## 📊 功能特色

- **智能波段识别**: 多周期协同分析
- **六维信号验证**: 趋势、动量、量能、资金、形态、环境
- **精准买卖点**: 基于量化模型的决策矩阵
- **动态仓位管理**: 底仓+加仓+补仓+T+0策略
- **完整风控体系**: 止盈、止损、时间、紧急四重保护

## 🔧 使用说明

1. 在左侧输入6位股票代码（如：000001）
2. 选择分析周期
3. 可选择设置持仓信息进行个性化分析
4. 点击"开始分析"查看完整报告

## 📱 跨平台支持

- ✅ Windows 10/11 (x64)
- ✅ macOS 10.14+ (Intel/Apple Silicon)
- ✅ Linux (Ubuntu 18.04+)

## ⚠️ 注意事项

1. **首次启动**: 可能需要较长时间，请耐心等待
2. **网络连接**: 需要网络连接获取股票数据
3. **防火墙**: 部分防火墙可能阻止应用启动，请添加信任
4. **端口占用**: 如果8501端口被占用，应用会自动寻找其他可用端口

## 🛠️ 故障排除

### 启动失败
- 检查是否有足够的磁盘空间（至少100MB）
- 尝试以管理员权限运行
- 临时关闭杀毒软件

### 浏览器未打开
- 手动打开浏览器访问控制台显示的地址
- 通常为: http://localhost:8501

### 数据获取失败
- 检查网络连接
- 确认股票代码格式正确（6位数字）

## 📞 技术支持

如遇问题请检查：
1. 系统兼容性
2. 网络连接状态
3. 防火墙设置
4. 磁盘空间

---

**免责声明**: 本工具仅供学习研究使用，不构成投资建议。投资有风险，决策需谨慎。
'''
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 说明文档创建完成")

def main():
    """主函数"""
    print("🚀 BandMaster Pro 自动化打包工具")
    print("=" * 50)
    
    # 检查依赖
    if not check_pyinstaller():
        return
    
    # 清理构建
    clean_build()
    
    # 创建入口文件
    create_main_entry()
    
    # 执行打包
    success = build_package()
    
    if success:
        # 创建启动脚本
        create_launcher_scripts()
        
        # 创建说明文档
        create_readme()
        
        print("\n" + "=" * 50)
        print("🎉 打包完成!")
        print("📁 输出目录: ./dist/")
        print("📄 可执行文件: BandMasterPro")
        print("📋 说明文档: README.md")
        print("🚀 启动脚本: 启动应用.bat / 启动应用.sh")
        print("=" * 50)
    else:
        print("\n❌ 打包失败，请检查错误信息")

if __name__ == "__main__":
    main() 