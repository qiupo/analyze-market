#!/usr/bin/env python3
"""
BandMaster Pro 开发环境启动脚本
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
    print("🚀 BandMaster Pro - 智策波段交易助手 (开发模式)")
    print("=" * 60)
    
    # 获取可用端口
    port = find_available_port()
    
    print(f"📡 启动服务...")
    print(f"🌐 访问地址: http://localhost:{port}")
    print("=" * 60)
    
    # 应用文件路径
    app_path = os.path.join('src', 'app.py')
    
    try:
        # 启动Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', str(port),
            '--server.headless', 'false',
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
            try:
                process.wait(timeout=5)  # 等待最多5秒
            except subprocess.TimeoutExpired:
                process.kill()  # 强制终止
            print("✅ 应用已停止")
        except SystemExit:
            print("\n🛑 应用退出...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("按回车键退出...")
        try:
            input()
        except:
            pass

if __name__ == "__main__":
    main() 