#!/usr/bin/env python3
"""
Docker容器化打包方案
适用于需要完全隔离环境的部署场景
"""

import os
import subprocess
import platform
from pathlib import Path

def create_dockerfile():
    """创建Dockerfile"""
    dockerfile_content = '''# BandMaster Pro Docker镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    wget \\
    && rm -rf /var/lib/apt/lists/*

# 安装TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \\
    tar -xzf ta-lib-0.4.0-src.tar.gz && \\
    cd ta-lib/ && \\
    ./configure --prefix=/usr && \\
    make && \\
    make install && \\
    cd .. && \\
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据和日志目录
RUN mkdir -p logs data

# 暴露端口
EXPOSE 8501

# 设置环境变量
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
'''
    
    with open('Dockerfile', 'w', encoding='utf-8') as f:
        f.write(dockerfile_content)
    print("✅ Dockerfile 创建完成")

def create_docker_compose():
    """创建docker-compose.yml"""
    compose_content = '''version: '3.8'

services:
  bandmaster-pro:
    build: .
    container_name: bandmaster-pro
    ports:
      - "8501:8501"
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
'''
    
    with open('docker-compose.yml', 'w', encoding='utf-8') as f:
        f.write(compose_content)
    print("✅ docker-compose.yml 创建完成")

def create_dockerignore():
    """创建.dockerignore"""
    dockerignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build artifacts
build/
dist/
*.egg-info/

# Git
.git/
.gitignore

# Logs
logs/
*.log

# Data files
data/
*.csv
*.xlsx

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Documentation
README.md
docs/
'''
    
    with open('.dockerignore', 'w', encoding='utf-8') as f:
        f.write(dockerignore_content)
    print("✅ .dockerignore 创建完成")

def create_docker_scripts():
    """创建Docker操作脚本"""
    
    # 构建脚本
    build_script = '''#!/bin/bash
echo "🐳 构建 BandMaster Pro Docker 镜像..."

# 构建镜像
docker build -t bandmaster-pro:latest .

if [ $? -eq 0 ]; then
    echo "✅ 镜像构建成功!"
    echo "📊 镜像信息:"
    docker images bandmaster-pro:latest
else
    echo "❌ 镜像构建失败!"
    exit 1
fi
'''
    
    with open('docker_build.sh', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # 运行脚本
    run_script = '''#!/bin/bash
echo "🚀 启动 BandMaster Pro..."

# 停止现有容器
docker-compose down

# 启动新容器
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ 应用启动成功!"
    echo "🌐 访问地址: http://localhost:8501"
    echo "📊 查看日志: docker-compose logs -f"
    echo "🛑 停止应用: docker-compose down"
else
    echo "❌ 应用启动失败!"
    exit 1
fi
'''
    
    with open('docker_run.sh', 'w', encoding='utf-8') as f:
        f.write(run_script)
    
    # Windows批处理
    build_bat = '''@echo off
echo 🐳 构建 BandMaster Pro Docker 镜像...

docker build -t bandmaster-pro:latest .

if %errorlevel% equ 0 (
    echo ✅ 镜像构建成功!
    docker images bandmaster-pro:latest
) else (
    echo ❌ 镜像构建失败!
    pause
)
'''
    
    with open('docker_build.bat', 'w', encoding='gbk') as f:
        f.write(build_bat)
    
    run_bat = '''@echo off
echo 🚀 启动 BandMaster Pro...

docker-compose down
docker-compose up -d

if %errorlevel% equ 0 (
    echo ✅ 应用启动成功!
    echo 🌐 访问地址: http://localhost:8501
    echo 📊 查看日志: docker-compose logs -f
    echo 🛑 停止应用: docker-compose down
) else (
    echo ❌ 应用启动失败!
    pause
)
'''
    
    with open('docker_run.bat', 'w', encoding='gbk') as f:
        f.write(run_bat)
    
    # 设置执行权限
    if platform.system() != 'Windows':
        os.chmod('docker_build.sh', 0o755)
        os.chmod('docker_run.sh', 0o755)
    
    print("✅ Docker操作脚本创建完成")

def create_docker_readme():
    """创建Docker部署说明"""
    readme_content = '''# BandMaster Pro - Docker 部署指南

## 🐳 Docker 容器化部署

使用Docker可以确保应用在任何支持Docker的系统上一致运行。

## 📋 前置要求

- Docker Engine 20.10+
- Docker Compose 1.29+
- 至少2GB可用内存
- 至少1GB可用磁盘空间

## 🚀 快速部署

### 方法一：使用脚本（推荐）

**Linux/macOS:**
```bash
# 构建镜像
./docker_build.sh

# 启动应用
./docker_run.sh
```

**Windows:**
```cmd
REM 构建镜像
docker_build.bat

REM 启动应用  
docker_run.bat
```

### 方法二：手动操作

```bash
# 1. 构建镜像
docker build -t bandmaster-pro:latest .

# 2. 启动应用
docker-compose up -d

# 3. 查看状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f

# 5. 停止应用
docker-compose down
```

## 🌐 访问应用

应用启动后访问: http://localhost:8501

## 📊 管理命令

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 重启应用
docker-compose restart

# 停止应用
docker-compose down

# 更新应用
docker-compose down
docker build -t bandmaster-pro:latest .
docker-compose up -d
```

## 🔧 配置选项

### 端口配置
在 `docker-compose.yml` 中修改端口映射：
```yaml
ports:
  - "8080:8501"  # 将8501改为8080
```

### 环境变量
```yaml
environment:
  - TZ=Asia/Shanghai          # 时区设置
  - STREAMLIT_THEME_BASE=dark # 主题设置
```

### 数据持久化
应用数据存储在以下目录：
- `./logs/` - 应用日志
- `./data/` - 数据缓存

## 📱 多平台支持

该Docker镜像支持以下架构：
- ✅ x86_64 (Intel/AMD)
- ✅ ARM64 (Apple Silicon/ARM服务器)

## 🛠️ 故障排除

### 端口冲突
```bash
# 查看端口占用
lsof -i :8501

# 修改docker-compose.yml中的端口
```

### 内存不足
```bash
# 检查Docker资源限制
docker system df
docker system prune  # 清理未使用的资源
```

### 构建失败
```bash
# 清理Docker缓存
docker builder prune

# 重新构建（无缓存）
docker build --no-cache -t bandmaster-pro:latest .
```

## 📦 生产环境部署

### 使用反向代理
配合Nginx使用：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 资源限制
```yaml
services:
  bandmaster-pro:
    # ... 其他配置
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

## ⚠️ 注意事项

1. **数据安全**: 容器重启数据不会丢失（已配置数据卷）
2. **网络访问**: 需要网络连接获取股票数据
3. **防火墙**: 确保8501端口可访问
4. **性能**: 首次启动可能需要较长时间

---

**技术支持**: 如遇问题请检查Docker日志和容器状态
'''
    
    with open('Docker_README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ Docker部署说明创建完成")

def main():
    """主函数"""
    print("🐳 BandMaster Pro Docker 打包工具")
    print("=" * 50)
    
    # 创建Docker文件
    create_dockerfile()
    create_docker_compose()
    create_dockerignore()
    create_docker_scripts()
    create_docker_readme()
    
    print("\n" + "=" * 50)
    print("🎉 Docker配置文件创建完成!")
    print("📁 生成的文件:")
    print("   📄 Dockerfile")
    print("   📄 docker-compose.yml")
    print("   📄 .dockerignore")
    print("   🚀 docker_build.sh/.bat")
    print("   🚀 docker_run.sh/.bat")
    print("   📋 Docker_README.md")
    print("\n🚀 快速开始:")
    print("   1. 运行 ./docker_build.sh 构建镜像")
    print("   2. 运行 ./docker_run.sh 启动应用")
    print("   3. 访问 http://localhost:8501")
    print("=" * 50)

if __name__ == "__main__":
    main() 