# BandMaster Pro - Linux版本

## 快速开始

### 方法1: 直接运行（推荐）
```bash
chmod +x run.sh
./run.sh
```

### 方法2: 手动运行
```bash
# 安装依赖
pip3 install -r requirements.txt

# 启动应用
python3 main.py
```

## 系统要求
- Linux系统（Ubuntu 18.04+, CentOS 7+, 等）
- Python 3.8+
- 网络连接（用于获取股票数据）

## 安装Python依赖
```bash
pip3 install streamlit akshare pandas numpy plotly requests python-dateutil colorama TA-Lib
```

## 使用说明
1. 运行后会自动打开浏览器
2. 在网页界面输入股票代码（如：000001）
3. 点击"开始分析"获取波段分析结果

## 故障排除
- 如果遇到权限问题：`chmod +x run.sh`
- 如果依赖安装失败：`pip3 install --upgrade pip`
- 如果端口被占用：程序会自动选择其他端口 