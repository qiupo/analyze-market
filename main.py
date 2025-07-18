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

def check_port_available(port):
    """检查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
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
        # 检查文件是否存在
        if not os.path.exists(app_path):
            print(f"❌ 应用文件不存在: {app_path}")
            print("按回车键退出...")
            try:
                input()
            except:
                pass
            return
    else:
        # 开发环境
        app_path = os.path.join('src', 'app.py')
        if not os.path.exists(app_path):
            print(f"❌ 应用文件不存在: {app_path}")
            print("按回车键退出...")
            try:
                input()
            except:
                pass
            return
    
    try:
        # 启动Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--server.runOnSave', 'false'
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
        max_wait_time = 30  # 最多等待30秒
        start_time = time.time()
        app_started = False
        
        while time.time() - start_time < max_wait_time:
            # 检查进程是否还在运行
            if process.poll() is not None:
                # 进程已退出
                stdout, stderr = process.communicate()
                print(f"❌ 应用启动失败")
                if stdout:
                    print(f"标准输出: {stdout}")
                if stderr:
                    print(f"错误输出: {stderr}")
                break
            
            # 检查端口是否被占用（表示应用已启动）
            if not check_port_available(port):
                # 端口被占用，应用可能已启动
                time.sleep(2)  # 再等2秒确保完全启动
                app_started = True
                break
            else:
                # 端口仍可用，继续等待
                time.sleep(1)
                continue
        
        if not app_started:
            print("❌ 应用启动超时")
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            print("按回车键退出...")
            try:
                input()
            except:
                pass
            return
        
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
        except KeyboardInterrupt:
            print("\n🛑 正在停止应用...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
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
