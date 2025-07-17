#!/usr/bin/env python3
"""
BandMaster Pro 启动器
用于PyInstaller打包后的应用启动
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

def get_local_ip():
    """获取本地IP地址"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return '127.0.0.1'

def main():
    """主启动函数"""
    print("=" * 60)
    print("🚀 BandMaster Pro - 智策波段交易助手")
    print("=" * 60)
    
    # 获取可用端口
    port = find_available_port()
    local_ip = get_local_ip()
    
    print(f"📡 启动服务...")
    print(f"🌐 本地访问: http://localhost:{port}")
    print(f"🌐 网络访问: http://{local_ip}:{port}")
    print("=" * 60)
    
    # 获取应用文件路径
    if getattr(sys, 'frozen', False):
        # 打包后的环境
        app_path = os.path.join(sys._MEIPASS, 'app.py')
    else:
        # 开发环境
        app_path = 'app.py'
    
    try:
        # 启动Streamlit应用
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', str(port),
            '--server.address', '0.0.0.0',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--theme.base', 'light'
        ]
        
        # 启动应用进程
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 等待应用启动
        print("⏳ 正在启动应用，请稍候...")
        time.sleep(5)
        
        # 自动打开浏览器
        webbrowser.open(f'http://localhost:{port}')
        print("✅ 应用已启动，浏览器将自动打开")
        print("💡 如果浏览器未自动打开，请手动访问上述网址")
        print("\n按 Ctrl+C 停止应用")
        
        # 等待进程结束
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 正在停止应用...")
            process.terminate()
            process.wait()
            print("✅ 应用已停止")
            
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
        print("💡 请检查是否有其他应用占用端口")
        input("按回车键退出...")

if __name__ == "__main__":
    main() 