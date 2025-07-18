#!/usr/bin/env python3
"""
智策波段交易助手启动脚本
BandMaster Pro Start Script
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """检查依赖包是否安装"""
    required_packages = [
        'streamlit',
        'akshare', 
        'pandas',
        'numpy',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def get_local_ip():
    """获取本地IP地址"""
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "localhost"

def start_application():
    """启动Streamlit应用"""
    print("🚀 正在启动智策波段交易助手...")
    print("=" * 50)
    
    # 设置Streamlit配置
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    
    # 启动应用
    try:
        # 构建启动命令
        cmd = [sys.executable, '-m', 'streamlit', 'run', 'src/app.py']
        
        # 添加配置参数
        cmd.extend([
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--server.headless', 'false',
            '--browser.gatherUsageStats', 'false'
        ])
        
        print("📊 启动命令:", ' '.join(cmd))
        print("🌐 访问地址: http://localhost:8501")
        print("🌐 局域网访问: http://{}:8501".format(get_local_ip()))
        print("=" * 50)
        print("💡 使用说明:")
        print("   1. 在左侧输入股票代码（如：000001）")
        print("   2. 选择分析周期")
        print("   3. 点击'开始分析'按钮")
        print("   4. 查看分析结果")
        print("=" * 50)
        print("⚠️  风险提示: 本系统仅供参考，投资有风险")
        print("🛑 停止服务: 按 Ctrl+C")
        print("=" * 50)
        
        # 启动应用
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("📈 智策波段交易助手 (BandMaster Pro)")
    print("版本: V1.0")
    print("作者: AI Assistant")
    print("=" * 50)
    
    # 检查当前目录
    current_dir = Path.cwd()
    app_file = current_dir / "src" / "app.py"
    
    if not app_file.exists():
        print("❌ 找不到 src/app.py 文件")
        print("请确保在项目根目录下运行此脚本")
        return
    
    print(f"📁 当前目录: {current_dir}")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 启动应用
    start_application()

if __name__ == "__main__":
    main() 