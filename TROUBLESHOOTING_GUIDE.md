# BandMaster Pro - 故障排除指南

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
type logs\app.log  # Windows

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
