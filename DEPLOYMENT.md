# 智策波段交易助手部署指南

## 概述

本指南提供了多种部署方式，从简单的本地部署到生产环境的服务器部署。

## 部署方式

### 1. 一键部署（推荐）

最简单的部署方式，支持Docker和传统部署：

```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行一键部署
./deploy.sh
```

脚本会自动检测系统环境并选择最适合的部署方式。

### 2. Docker部署

#### 开发环境
```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 生产环境
```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d
```

### 3. 传统部署

#### 本地部署
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动应用
python start.py
```

#### 服务器部署
```bash
# 运行服务器部署脚本
chmod +x server-deploy.sh
./server-deploy.sh
```

## 系统要求

### 最低要求
- Python 3.8+
- 2GB RAM
- 1GB 磁盘空间

### 推荐配置
- Python 3.9+
- 4GB RAM
- 5GB 磁盘空间
- Docker 20.10+

## 端口配置

- **8501**: Streamlit应用端口
- **80**: HTTP端口（Nginx）
- **443**: HTTPS端口（Nginx）

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| STREAMLIT_SERVER_PORT | 8501 | Streamlit服务端口 |
| STREAMLIT_SERVER_ADDRESS | 0.0.0.0 | 服务监听地址 |
| STREAMLIT_SERVER_HEADLESS | true | 无头模式 |
| STREAMLIT_BROWSER_GATHER_USAGE_STATS | false | 禁用使用统计 |

## 服务管理

### Docker方式
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### Systemd方式
```bash
# 启动服务
sudo systemctl start stock-analyzer

# 停止服务
sudo systemctl stop stock-analyzer

# 重启服务
sudo systemctl restart stock-analyzer

# 查看状态
sudo systemctl status stock-analyzer

# 查看日志
sudo journalctl -u stock-analyzer -f

# 设置开机自启
sudo systemctl enable stock-analyzer
```

## 监控和维护

### 健康检查
应用提供健康检查端点：
- Docker: `http://localhost:8501/_stcore/health`
- Nginx: `http://localhost/health`

### 日志管理
- 应用日志: `./logs/`
- Nginx日志: `./logs/nginx/`
- 系统日志: `sudo journalctl -u stock-analyzer`

### 备份
```bash
# 备份应用数据
tar -czf stock-analyzer-backup-$(date +%Y%m%d).tar.gz \
    --exclude=venv \
    --exclude=__pycache__ \
    --exclude=logs \
    .
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tulpn | grep 8501
   
   # 杀死进程
   sudo kill -9 <PID>
   ```

2. **Docker权限问题**
   ```bash
   # 添加用户到docker组
   sudo usermod -aG docker $USER
   
   # 重新登录
   logout
   ```

3. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 清理缓存
   pip cache purge
   
   # 重新安装
   pip install -r requirements.txt --force-reinstall
   ```

4. **内存不足**
   ```bash
   # 增加swap空间
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

### 性能优化

1. **增加缓存**
   - 调整Streamlit缓存时间
   - 使用Redis缓存（可选）

2. **负载均衡**
   - 使用Nginx反向代理
   - 配置多个应用实例

3. **数据库优化**
   - 使用连接池
   - 优化查询语句

## 安全配置

### 防火墙设置
```bash
# Ubuntu/Debian
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8501/tcp

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

### SSL证书（可选）
```bash
# 使用Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 更新部署

### 代码更新
```bash
# 拉取最新代码
git pull origin main

# 重新部署
./deploy.sh
```

### 依赖更新
```bash
# 更新requirements.txt后
pip install -r requirements.txt --upgrade

# 或使用Docker
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 联系支持

如遇到部署问题，请检查：
1. 系统要求是否满足
2. 网络连接是否正常
3. 端口是否被占用
4. 日志文件中的错误信息

---

**注意**: 本系统仅供参考，投资有风险，请谨慎使用。 