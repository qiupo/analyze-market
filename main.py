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
import signal
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

def signal_handler(signum, frame):
    """信号处理器"""
    global streamlit_process
    if streamlit_process:
        print("\n🛑 收到退出信号，正在停止应用...")
        streamlit_process.terminate()
        try:
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            streamlit_process.kill()
        print("✅ 应用已停止")
    sys.exit(0)

def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("🚀 BandMaster Pro - 智策波段交易助手")
    print("=" * 60)
    
    # 获取可用端口
    port = find_available_port()
    
    print(f"📡 启动服务...")
    print(f"🌐 访问地址: http://localhost:{port}")
    print("=" * 60)
    
    # 全局变量存储进程
    global streamlit_process
    streamlit_process = None
    
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
        streamlit_process = process
        
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
