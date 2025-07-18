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

def check_port_in_use(port):
    """检查端口是否被占用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', port))
            return True
    except OSError:
        return False

def wait_for_server(port, process, timeout=30):
    """等待服务器启动"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        # 检查进程是否还在运行
        if process.poll() is not None:
            # 进程已退出，启动失败
            return False
        
        # 检查端口是否被占用
        if check_port_in_use(port):
            return True
        time.sleep(1)
    return False

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
    
    while True:
        try:
            print("=" * 60)
            print("🚀 BandMaster Pro - 智策波段交易助手 (开发模式)")
            print("=" * 60)
            
            # 获取可用端口
            port = find_available_port()
            
            print(f"📡 启动服务...")
            print(f"🌐 访问地址: http://localhost:{port}")
            print("=" * 60)
            
            # 全局变量存储进程
            global streamlit_process
            streamlit_process = None
            
            # 应用文件路径
            app_path = os.path.join('src', 'app.py')
            
            # 检查文件是否存在
            if not os.path.exists(app_path):
                print(f"❌ 应用文件不存在: {app_path}")
                print("请确保在项目根目录中运行此脚本")
                print("按回车键退出...")
                try:
                    input()
                except:
                    pass
                return
            
            # 启动Streamlit
            cmd = [
                sys.executable, '-m', 'streamlit', 'run', app_path,
                '--server.port', str(port),
                '--server.headless', 'false',
                '--browser.gatherUsageStats', 'false',
                '--server.runOnSave', 'true'
            ]
            
            print("⏳ 正在启动应用...")
            
            # 使用subprocess.Popen启动进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            streamlit_process = process
            
            # 等待应用启动
            print("⏳ 等待服务器启动...")
            app_started = wait_for_server(port, process, timeout=30)
            
            if not app_started:
                print("❌ 应用启动超时")
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                print("按回车键重新启动，或按Ctrl+C退出...")
                try:
                    input()
                    continue
                except KeyboardInterrupt:
                    print("\n✅ 应用已退出")
                    break
            
            print("✅ 应用已启动")
            print("\n按 Ctrl+C 停止应用")
            
            # 打开浏览器
            try:
                webbrowser.open(f'http://localhost:{port}')
            except Exception as e:
                print(f"⚠️ 无法自动打开浏览器: {e}")
                print(f"请手动访问: http://localhost:{port}")
            
            # 等待进程结束
            try:
                process.wait()
                # Streamlit进程已退出，但主进程不要退出
                print("\n🔄 Streamlit进程已退出")
                print("按回车键重新启动，或按Ctrl+C退出...")
                try:
                    input()
                    # 重新启动
                    print("🔄 重新启动应用...")
                    continue
                except KeyboardInterrupt:
                    print("\n✅ 应用已退出")
                    break
            except KeyboardInterrupt:
                print("\n🛑 正在停止应用...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print("✅ 应用已停止")
                break
            except SystemExit:
                print("\n🛑 应用退出...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                break
                
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            print("按回车键重新启动，或按Ctrl+C退出...")
            try:
                input()
                continue
            except KeyboardInterrupt:
                print("\n✅ 应用已退出")
                break

if __name__ == "__main__":
    main() 