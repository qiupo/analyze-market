#!/usr/bin/env python3
"""
BandMaster Pro 部署指南生成器
创建详细的跨平台部署说明
"""

import os
import platform
from pathlib import Path

def create_main_deployment_guide():
    """创建主部署指南"""
    guide_content = '''# BandMaster Pro - 完整部署指南

## 🚀 概述

BandMaster Pro 是一个基于Streamlit的股票波段分析系统，提供多种部署方案以适应不同的使用场景和技术需求。

## 📋 部署方案对比

| 方案 | 适用场景 | 技术要求 | 部署难度 | 性能 | 维护性 |
|------|----------|----------|----------|------|--------|
| **便携式包** | 个人使用、演示 | 无 | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| **PyInstaller** | 单机部署、分发 | 基础 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Docker** | 服务器部署、云端 | 中等 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **源码部署** | 开发、定制 | 高 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🎯 选择建议

### 新手用户 → 便携式包
- ✅ 无需技术背景
- ✅ 下载即用
- ✅ 适合试用体验

### 个人长期使用 → PyInstaller
- ✅ 启动速度快
- ✅ 系统集成好
- ✅ 资源占用少

### 团队/企业使用 → Docker
- ✅ 环境一致性
- ✅ 易于扩展
- ✅ 便于维护

### 开发者 → 源码部署
- ✅ 完全控制
- ✅ 便于定制
- ✅ 适合二次开发

## 📱 平台支持矩阵

| 平台 | 便携式包 | PyInstaller | Docker | 源码部署 |
|------|----------|-------------|--------|----------|
| **Windows 10/11** | ✅ | ✅ | ✅ | ✅ |
| **macOS Intel** | ✅ | ✅ | ✅ | ✅ |
| **macOS Apple Silicon** | ✅ | ✅ | ✅ | ✅ |
| **Ubuntu 18.04+** | ✅ | ✅ | ✅ | ✅ |
| **CentOS 7+** | ⚠️ | ⚠️ | ✅ | ✅ |
| **Debian 10+** | ✅ | ✅ | ✅ | ✅ |

注: ⚠️ 表示需要额外配置

---

## 🏗️ 部署方案详解

### 方案一：便携式包部署

**适用场景**: 快速试用、个人使用、无Python环境

**优势**:
- 🚀 开箱即用，无需安装
- 📦 包含完整运行环境
- 🔒 环境隔离，不影响系统

**步骤**:
1. 运行打包脚本: `python portable_package.py`
2. 解压生成的便携式包
3. 双击启动脚本即可使用

**文件结构**:
```
BandMaster-Pro-Portable/
├── 启动应用.bat/.sh    # 启动脚本
├── portable_env/       # Python环境
├── app.py             # 应用文件
├── logs/              # 日志目录
└── Portable_README.md # 说明文档
```

---

### 方案二：PyInstaller独立程序

**适用场景**: 单机部署、程序分发、生产环境

**优势**:
- ⚡ 启动速度最快
- 📦 单文件分发
- 🎯 针对目标平台优化

**步骤**:
1. 安装打包依赖: `pip install -r requirements_build.txt`
2. 运行打包脚本: `python build_package.py`
3. 在`dist/`目录获取可执行文件

**输出文件**:
- `BandMasterPro.exe` (Windows)
- `BandMasterPro` (Linux/macOS)
- 启动脚本和说明文档

---

### 方案三：Docker容器化部署

**适用场景**: 服务器部署、云环境、团队协作

**优势**:
- 🐳 环境完全一致
- 🔄 易于更新维护
- 📈 支持横向扩展
- 🛡️ 安全隔离

**快速部署**:
```bash
# 1. 生成Docker配置
python docker_package.py

# 2. 构建镜像
./docker_build.sh

# 3. 启动服务
./docker_run.sh
```

**管理命令**:
```bash
# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 更新应用
docker-compose down
docker build -t bandmaster-pro:latest .
docker-compose up -d
```

---

### 方案四：源码直接部署

**适用场景**: 开发环境、定制需求、学习研究

**优势**:
- 🛠️ 完全可定制
- 🔍 便于调试
- 📚 学习代码结构

**部署步骤**:
```bash
# 1. 克隆代码
git clone <repository>
cd analyzeMarket

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活环境
# Windows: venv\\Scripts\\activate
# Linux/macOS: source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 启动应用
streamlit run app.py
```

---

## 🔧 环境配置指南

### Python环境要求
- **版本**: Python 3.8+
- **建议**: Python 3.10 (最佳兼容性)

### 系统依赖

**Windows**:
```bash
# 安装TA-Lib (可选，用于高级技术分析)
# 下载whl文件: https://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install TA_Lib‑0.4.XX‑cpXX‑cpXX‑win_amd64.whl
```

**macOS**:
```bash
# 使用Homebrew安装TA-Lib
brew install ta-lib
pip install TA-Lib
```

**Ubuntu/Debian**:
```bash
# 安装编译依赖
sudo apt-get update
sudo apt-get install build-essential
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
```

---

## 🔍 故障排除

### 常见问题解决

**1. TA-Lib安装失败**
```bash
# 解决方案1: 使用conda
conda install -c conda-forge ta-lib

# 解决方案2: 跳过TA-Lib
# 修改requirements.txt，注释或删除TA-Lib行
```

**2. 端口占用问题**
```bash
# 查看端口占用
netstat -tulpn | grep 8501

# 指定其他端口启动
streamlit run app.py --server.port 8502
```

**3. 内存不足**
```bash
# 监控内存使用
htop  # Linux
taskmgr  # Windows

# 调整Streamlit配置
# .streamlit/config.toml
[server]
maxUploadSize = 200
maxMessageSize = 200
```

**4. 网络连接问题**
```bash
# 测试网络连接
ping baidu.com

# 检查代理设置
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

### 性能优化

**1. 缓存优化**
```python
# 增加缓存时间
@st.cache_data(ttl=600)  # 10分钟缓存
def load_data():
    pass
```

**2. 内存管理**
```python
# 定期清理缓存
if st.button("清理缓存"):
    st.cache_data.clear()
```

**3. 数据加载优化**
```python
# 异步数据加载
import asyncio
async def fetch_data():
    pass
```

---

## 🔒 安全配置

### 生产环境安全

**1. HTTPS配置**
```bash
# 使用Nginx反向代理
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
    }
}
```

**2. 访问控制**
```python
# Streamlit认证
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    names, usernames, hashed_passwords,
    'app_name', 'signature_key'
)

name, authentication_status, username = authenticator.login()
```

**3. 环境变量**
```bash
# 敏感信息使用环境变量
export STOCK_API_KEY=your_api_key
export DATABASE_URL=your_db_url
```

---

## 📊 监控运维

### 日志管理
```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### 健康检查
```bash
# 应用健康检查
curl http://localhost:8501/_stcore/health

# Docker健康检查
docker-compose ps
```

### 备份策略
```bash
# 数据备份
tar -czf backup_$(date +%Y%m%d).tar.gz logs/ data/

# 定期备份脚本
0 2 * * * /path/to/backup.sh
```

---

## 📞 技术支持

### 问题报告模板
```
**环境信息**:
- 操作系统: 
- Python版本:
- 部署方案:

**问题描述**:
- 现象:
- 预期结果:
- 实际结果:

**重现步骤**:
1. 
2. 
3. 

**日志信息**:
```

### 获取帮助
1. 查看本地日志文件
2. 检查网络连接状态
3. 验证系统环境配置
4. 尝试重启应用服务

---

**免责声明**: 本部署指南仅供技术参考，请根据实际环境调整配置。使用过程中请注意数据安全和系统稳定性。
'''
    
    with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ 主部署指南创建完成")

def create_quick_start_scripts():
    """创建快速启动脚本"""
    print("📝 创建快速启动脚本...")
    
    # Windows一键部署脚本
    windows_script = '''@echo off
title BandMaster Pro - 一键部署工具
chcp 65001 >nul

echo.
echo ========================================
echo   BandMaster Pro - 一键部署工具
echo ========================================
echo.

:MENU
echo 请选择部署方案:
echo.
echo 1. 便携式包 (推荐新手)
echo 2. PyInstaller独立程序
echo 3. Docker容器化
echo 4. 源码直接运行
echo 5. 查看部署指南
echo 6. 退出
echo.
set /p choice=请输入选项 (1-6): 

if "%choice%"=="1" goto PORTABLE
if "%choice%"=="2" goto PYINSTALLER  
if "%choice%"=="3" goto DOCKER
if "%choice%"=="4" goto SOURCE
if "%choice%"=="5" goto GUIDE
if "%choice%"=="6" goto EXIT

echo 无效选项，请重新选择
goto MENU

:PORTABLE
echo.
echo 🚀 开始创建便携式包...
python portable_package.py
if %errorlevel% equ 0 (
    echo ✅ 便携式包创建完成!
) else (
    echo ❌ 便携式包创建失败
)
pause
goto MENU

:PYINSTALLER
echo.
echo 🚀 开始PyInstaller打包...
python build_package.py
if %errorlevel% equ 0 (
    echo ✅ PyInstaller打包完成!
) else (
    echo ❌ PyInstaller打包失败
)
pause
goto MENU

:DOCKER
echo.
echo 🚀 开始Docker容器化...
python docker_package.py
if %errorlevel% equ 0 (
    echo ✅ Docker配置文件创建完成!
    echo 💡 请运行 docker_build.bat 构建镜像
) else (
    echo ❌ Docker配置创建失败
)
pause
goto MENU

:SOURCE
echo.
echo 🚀 直接运行源码...
pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo ✅ 依赖安装完成，启动应用...
    streamlit run app.py
) else (
    echo ❌ 依赖安装失败
)
pause
goto MENU

:GUIDE
echo.
echo 📋 打开部署指南...
if exist "DEPLOYMENT_GUIDE.md" (
    start DEPLOYMENT_GUIDE.md
) else (
    echo ❌ 部署指南文件不存在
    echo 💡 请先运行 python deployment_guide.py 创建指南
)
pause
goto MENU

:EXIT
echo.
echo 👋 感谢使用 BandMaster Pro!
exit /b 0
'''
    
    with open('一键部署.bat', 'w', encoding='utf-8') as f:
        f.write(windows_script)
    
    # Unix系统一键部署脚本
    unix_script = '''#!/bin/bash

echo "========================================"
echo "  BandMaster Pro - 一键部署工具"
echo "========================================"
echo

show_menu() {
    echo "请选择部署方案:"
    echo
    echo "1. 便携式包 (推荐新手)"
    echo "2. PyInstaller独立程序"
    echo "3. Docker容器化"
    echo "4. 源码直接运行"
    echo "5. 查看部署指南"
    echo "6. 退出"
    echo
}

while true; do
    show_menu
    read -p "请输入选项 (1-6): " choice
    
    case $choice in
        1)
            echo
            echo "🚀 开始创建便携式包..."
            python3 portable_package.py
            if [ $? -eq 0 ]; then
                echo "✅ 便携式包创建完成!"
            else
                echo "❌ 便携式包创建失败"
            fi
            read -p "按回车键继续..."
            ;;
        2)
            echo
            echo "🚀 开始PyInstaller打包..."
            python3 build_package.py
            if [ $? -eq 0 ]; then
                echo "✅ PyInstaller打包完成!"
            else
                echo "❌ PyInstaller打包失败"
            fi
            read -p "按回车键继续..."
            ;;
        3)
            echo
            echo "🚀 开始Docker容器化..."
            python3 docker_package.py
            if [ $? -eq 0 ]; then
                echo "✅ Docker配置文件创建完成!"
                echo "💡 请运行 ./docker_build.sh 构建镜像"
            else
                echo "❌ Docker配置创建失败"
            fi
            read -p "按回车键继续..."
            ;;
        4)
            echo
            echo "🚀 直接运行源码..."
            pip3 install -r requirements.txt
            if [ $? -eq 0 ]; then
                echo "✅ 依赖安装完成，启动应用..."
                streamlit run app.py
            else
                echo "❌ 依赖安装失败"
            fi
            read -p "按回车键继续..."
            ;;
        5)
            echo
            echo "📋 打开部署指南..."
            if [ -f "DEPLOYMENT_GUIDE.md" ]; then
                if command -v open &> /dev/null; then
                    open DEPLOYMENT_GUIDE.md
                elif command -v xdg-open &> /dev/null; then
                    xdg-open DEPLOYMENT_GUIDE.md
                else
                    echo "请手动打开 DEPLOYMENT_GUIDE.md 文件"
                fi
            else
                echo "❌ 部署指南文件不存在"
                echo "💡 请先运行 python3 deployment_guide.py 创建指南"
            fi
            read -p "按回车键继续..."
            ;;
        6)
            echo
            echo "👋 感谢使用 BandMaster Pro!"
            exit 0
            ;;
        *)
            echo "无效选项，请重新选择"
            ;;
    esac
    
    echo
done
'''
    
    with open('一键部署.sh', 'w', encoding='utf-8') as f:
        f.write(unix_script)
    
    # 设置执行权限
    if platform.system() != 'Windows':
        os.chmod('一键部署.sh', 0o755)
    
    print("✅ 快速启动脚本创建完成")

def create_troubleshooting_guide():
    """创建故障排除指南"""
    troubleshooting_content = '''# BandMaster Pro - 故障排除指南

## 🔧 常见问题快速解决

### 📋 问题分类索引

- [安装问题](#安装问题)
- [启动问题](#启动问题)
- [运行问题](#运行问题)
- [性能问题](#性能问题)
- [网络问题](#网络问题)
- [数据问题](#数据问题)

---

## 安装问题

### 问题1: Python环境问题
**现象**: 提示Python版本不兼容
**解决方案**:
```bash
# 检查Python版本
python --version
python3 --version

# 需要Python 3.8+
# 如果版本过低，请升级Python
```

### 问题2: pip安装依赖失败
**现象**: pip install 报错
**解决方案**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 单独安装问题包
pip install --no-cache-dir package_name
```

### 问题3: TA-Lib安装失败
**现象**: 编译错误或找不到库文件
**解决方案**:

**Windows**:
```bash
# 下载预编译包
# https://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install TA_Lib-0.4.XX-cpXX-cpXX-win_amd64.whl
```

**macOS**:
```bash
# 使用Homebrew
brew install ta-lib
pip install TA-Lib
```

**Linux**:
```bash
# 安装系统依赖
sudo apt-get install build-essential
# 编译安装TA-Lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make && sudo make install
```

---

## 启动问题

### 问题1: 启动脚本无反应
**现象**: 双击启动脚本没有反应

**Windows解决方案**:
```bash
# 1. 右键选择"以管理员身份运行"
# 2. 检查文件关联
# 3. 手动运行命令
cd /d "应用目录"
python app.py
```

**Linux/macOS解决方案**:
```bash
# 1. 添加执行权限
chmod +x 启动应用.sh

# 2. 检查脚本路径
cd /path/to/app
./启动应用.sh

# 3. 手动运行
python3 app.py
```

### 问题2: 端口被占用
**现象**: 提示端口8501已被使用
**解决方案**:
```bash
# 查看端口占用
netstat -tulpn | grep 8501  # Linux
netstat -ano | findstr 8501  # Windows

# 杀死占用进程
sudo kill -9 PID  # Linux
taskkill /F /PID PID  # Windows

# 或使用其他端口
streamlit run app.py --server.port 8502
```

### 问题3: 模块导入失败
**现象**: ModuleNotFoundError
**解决方案**:
```bash
# 1. 检查虚拟环境
which python  # 确认Python路径

# 2. 重新安装依赖
pip install -r requirements.txt

# 3. 检查PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/app"
```

---

## 运行问题

### 问题1: 页面加载失败
**现象**: 浏览器显示连接错误
**解决方案**:
```bash
# 1. 检查服务状态
ps aux | grep streamlit  # Linux
tasklist | findstr python  # Windows

# 2. 检查防火墙设置
# Windows: 控制面板 > 系统和安全 > Windows防火墙
# Linux: sudo ufw status

# 3. 手动打开浏览器
# 访问 http://localhost:8501
```

### 问题2: 应用崩溃
**现象**: 应用突然停止或出现错误页面
**解决方案**:
```bash
# 1. 查看错误日志
tail -f logs/app.log  # Linux
type logs\\app.log  # Windows

# 2. 重启应用
# 关闭当前进程，重新启动

# 3. 清理缓存
# 删除 .streamlit/cache 目录
```

### 问题3: 功能异常
**现象**: 某些功能不工作或显示异常
**解决方案**:
```bash
# 1. 清除浏览器缓存
# Ctrl+F5 强制刷新

# 2. 清除应用缓存
# 在应用中点击"清除缓存"按钮

# 3. 检查数据文件
# 确认data/目录下文件完整
```

---

## 性能问题

### 问题1: 启动速度慢
**现象**: 应用启动需要很长时间
**优化方案**:
```python
# 1. 减少导入的库
# 只导入必要的模块

# 2. 优化缓存配置
@st.cache_data(ttl=3600)  # 增加缓存时间
def load_data():
    pass

# 3. 使用懒加载
@st.cache_resource
def get_analyzer():
    return TechnicalAnalyzer()
```

### 问题2: 内存占用高
**现象**: 系统内存不足
**解决方案**:
```python
# 1. 定期清理缓存
if st.button("清理内存"):
    st.cache_data.clear()
    st.cache_resource.clear()

# 2. 限制数据量
# 减少历史数据获取天数

# 3. 优化数据结构
# 使用更少内存的数据类型
```

### 问题3: 响应速度慢
**现象**: 操作响应延迟
**优化方案**:
```python
# 1. 异步处理
import asyncio
async def fetch_data():
    pass

# 2. 分页加载
# 大量数据分批显示

# 3. 预加载数据
# 后台预先获取常用数据
```

---

## 网络问题

### 问题1: 无法获取数据
**现象**: 股票数据获取失败
**解决方案**:
```bash
# 1. 检查网络连接
ping baidu.com

# 2. 检查代理设置
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=https://proxy:port

# 3. 更换数据源
# 修改配置文件中的API地址
```

### 问题2: 请求超时
**现象**: 网络请求超时
**解决方案**:
```python
# 1. 增加超时时间
import requests
requests.get(url, timeout=30)

# 2. 添加重试机制
import time
for i in range(3):
    try:
        response = requests.get(url)
        break
    except:
        time.sleep(1)

# 3. 使用镜像服务
# 配置备用数据源
```

### 问题3: SSL证书错误
**现象**: HTTPS连接失败
**解决方案**:
```python
# 1. 更新证书
pip install --upgrade certifi

# 2. 禁用SSL验证（不推荐）
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 3. 使用HTTP代替HTTPS
# 修改请求URL
```

---

## 数据问题

### 问题1: 股票代码无效
**现象**: 提示股票代码不存在
**解决方案**:
```bash
# 1. 检查代码格式
# A股: 6位数字 (000001)
# 港股: 5位数字 (00700)

# 2. 验证代码有效性
# 在其他财经网站确认代码

# 3. 尝试不同格式
# 添加前缀: SH000001, SZ000001
```

### 问题2: 数据不准确
**现象**: 显示的数据与其他平台不一致
**解决方案**:
```bash
# 1. 检查数据源
# 确认使用的是哪个数据提供商

# 2. 对比时间戳
# 确认数据更新时间

# 3. 清除缓存
# 强制重新获取数据
```

### 问题3: 历史数据缺失
**现象**: 无法获取足够的历史数据
**解决方案**:
```python
# 1. 调整获取周期
period = 200  # 增加获取天数

# 2. 分段获取
# 分多次请求获取长期数据

# 3. 使用备用接口
# 配置多个数据源
```

---

## 🛠️ 调试工具

### 日志分析
```bash
# 查看实时日志
tail -f logs/app.log

# 查看错误日志
grep "ERROR" logs/app.log

# 查看特定时间日志
grep "2024-01-01" logs/app.log
```

### 系统诊断
```bash
# 检查Python环境
python --version
pip list

# 检查系统资源
# Linux: htop, free -h, df -h
# Windows: 任务管理器

# 检查网络连接
curl -I http://baidu.com
```

### 性能监控
```python
# 添加性能监控代码
import time
import psutil

start_time = time.time()
# 执行函数
end_time = time.time()
print(f"执行时间: {end_time - start_time:.2f}秒")

# 内存使用情况
process = psutil.Process()
print(f"内存使用: {process.memory_info().rss / 1024 / 1024:.2f}MB")
```

---

## 📞 获取帮助

### 自检清单
- [ ] Python版本 >= 3.8
- [ ] 所有依赖已安装
- [ ] 网络连接正常
- [ ] 端口8501可用
- [ ] 有足够磁盘空间
- [ ] 防火墙允许访问

### 收集诊断信息
```bash
# 生成诊断报告
python -c "
import sys, platform, subprocess
print('系统信息:')
print(f'操作系统: {platform.system()} {platform.release()}')
print(f'Python版本: {sys.version}')
print('已安装包:')
subprocess.run([sys.executable, '-m', 'pip', 'list'])
"
```

### 问题反馈格式
```
**环境信息**:
- 操作系统: 
- Python版本: 
- 部署方式: 

**问题描述**:
- 现象: 
- 触发条件: 
- 错误信息: 

**复现步骤**:
1. 
2. 
3. 

**日志信息**:
(粘贴相关日志)

**已尝试的解决方案**:
- 
- 
```

---

**提示**: 遇到问题时，请先查看日志文件，90%的问题都能从日志中找到原因。保持耐心，大多数问题都有解决方案！
'''
    
    with open('TROUBLESHOOTING_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(troubleshooting_content)
    
    print("✅ 故障排除指南创建完成")

def main():
    """主函数"""
    print("📋 BandMaster Pro 部署指南生成器")
    print("=" * 50)
    
    # 创建各种指南和脚本
    create_main_deployment_guide()
    create_quick_start_scripts()
    create_troubleshooting_guide()
    
    print("\n" + "=" * 50)
    print("🎉 部署指南生成完成!")
    print("📁 生成的文件:")
    print("   📋 DEPLOYMENT_GUIDE.md - 完整部署指南")
    print("   📋 TROUBLESHOOTING_GUIDE.md - 故障排除指南") 
    print("   🚀 一键部署.bat/.sh - 快速部署脚本")
    print("\n💡 使用建议:")
    print("   1. 先阅读 DEPLOYMENT_GUIDE.md 了解各种方案")
    print("   2. 运行 一键部署.bat/.sh 选择合适的部署方案")
    print("   3. 遇到问题时参考 TROUBLESHOOTING_GUIDE.md")
    print("=" * 50)

if __name__ == "__main__":
    main() 