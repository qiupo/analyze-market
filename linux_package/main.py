#!/usr/bin/env python3
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
        app_path = os.path.join(base_path, 'src', 'app.py')
    else:
        # 开发环境
        app_path = os.path.join('src', 'app.py')
    
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
        print("\n按 Ctrl+C 停止应用")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 正在停止应用...")
            process.terminate()
            print("✅ 应用已停止")
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
