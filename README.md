# 🚀 BandMaster Pro - 智策波段交易助手

## 📋 项目简介

BandMaster Pro 是一个基于人工智能的股票波段分析系统，通过多维度技术分析，为用户提供精准的买卖点建议和风险控制策略。

## 🎯 核心功能

- **智能波段识别**: 多周期协同分析，精准识别波段机会
- **六维信号验证**: 趋势、动量、量能、资金、形态、环境全方位分析
- **精准买卖点**: 基于量化模型的决策矩阵，提供明确的操作建议
- **动态仓位管理**: 底仓+加仓+补仓+T+0策略，灵活应对市场变化
- **完整风控体系**: 止盈、止损、时间、紧急四重保护机制

## 📁 项目结构

```
analyzeMarket/
├── 📁 src/                          # 源代码目录
│   ├── app.py                       # 主应用文件 (Streamlit)
│   ├── start.py                     # 启动脚本
│   ├── 📁 core/                     # 核心功能模块
│   │   ├── data_fetcher.py          # 数据获取模块
│   │   ├── technical_analysis.py    # 技术分析模块
│   │   ├── visualization.py         # 可视化模块
│   │   └── config.py                # 配置模块
│   └── 📁 utils/                    # 工具模块
│
├── 📁 build/                        # 构建相关文件
│   ├── 📁 scripts/                  # 构建脚本
│   ├── 📁 configs/                  # 构建配置
│   └── 📁 docs/                     # 构建文档
│
├── 📁 deploy/                       # 部署相关文件
│   ├── 📁 scripts/                  # 部署脚本
│   ├── 📁 configs/                  # 部署配置
│   └── 📁 docs/                     # 部署文档
│
├── 📁 docs/                         # 项目文档
├── 📁 .github/                      # GitHub配置
└── 📄 项目结构说明.md               # 详细结构说明
```

## 🚀 快速开始

### 开发环境运行

```bash
# 1. 克隆项目
git clone <repository-url>
cd analyzeMarket

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动开发环境
python run.py
```

### 跨平台构建

#### 方案一：GitHub Actions (推荐)

1. **推送代码到GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git push -u origin main
   ```

2. **启用GitHub Actions**
   - 在GitHub仓库页面点击 "Actions"
   - 点击 "New workflow" → "set up a workflow yourself"
   - 复制 `.github/workflows/build.yml` 的内容
   - 点击 "Commit changes"

3. **自动构建**
   - 每次推送代码到main分支时自动构建
   - 在 "Releases" 页面下载构建结果

#### 方案二：本地构建

```bash
# 使用跨平台构建工具
python build/scripts/build_cross_platform.py

# 或使用一键构建脚本
./build/scripts/一键跨平台构建.sh  # macOS/Linux
build/scripts/一键跨平台构建.bat   # Windows
```

### 部署

```bash
# 使用部署脚本
./deploy/scripts/deploy.sh

# 或使用一键部署
./deploy/scripts/一键部署.sh       # macOS/Linux
deploy/scripts/一键部署.bat        # Windows
```

## 📦 构建结果

构建完成后会生成以下文件：

- **Windows**: `BandMasterPro.exe` + `启动应用.bat`
- **Linux**: `BandMasterPro` + `启动应用.sh`
- **macOS**: `BandMasterPro` + `启动应用.sh`

## 🔧 系统要求

### 开发环境
- Python 3.8+
- 8GB+ RAM
- 2GB+ 可用磁盘空间

### 运行环境
- **Windows**: Windows 10/11 (x64)
- **Linux**: Ubuntu 18.04+ / CentOS 7+
- **macOS**: macOS 10.14+ (Intel/Apple Silicon)

## 📊 使用说明

1. **输入股票代码**: 在左侧输入6位股票代码（如：000001）
2. **选择分析周期**: 选择适合的分析周期
3. **设置持仓信息**: 可选择设置持仓信息进行个性化分析
4. **开始分析**: 点击"开始分析"查看完整报告

## ⚠️ 注意事项

1. **首次启动**: 可能需要10-30秒，请耐心等待
2. **网络连接**: 需要网络连接获取股票数据
3. **防火墙**: 部分防火墙可能阻止应用启动，请添加信任
4. **端口占用**: 如果8501端口被占用，应用会自动寻找其他可用端口

## 🛠️ 故障排除

### 常见问题

**启动失败**
- 检查是否有足够的磁盘空间（至少100MB）
- 尝试以管理员权限运行
- 临时关闭杀毒软件

**浏览器未打开**
- 手动打开浏览器访问控制台显示的地址
- 通常为: http://localhost:8501

**数据获取失败**
- 检查网络连接
- 确认股票代码格式正确（6位数字）

## 📖 详细文档

- **项目结构**: [项目结构说明.md](项目结构说明.md)
- **跨平台构建**: [build/docs/跨平台构建说明.md](build/docs/跨平台构建说明.md)
- **部署指南**: [deploy/docs/DEPLOYMENT_GUIDE.md](deploy/docs/DEPLOYMENT_GUIDE.md)
- **故障排除**: [deploy/docs/TROUBLESHOOTING_GUIDE.md](deploy/docs/TROUBLESHOOTING_GUIDE.md)

## 🔒 安全说明

- 本工具仅获取公开股票数据
- 不上传任何用户个人信息
- 所有分析在本地进行
- 建议在可信网络环境下使用

## 📞 技术支持

如遇问题请检查：
1. 系统兼容性
2. 网络连接状态
3. 防火墙设置
4. 磁盘空间

## 📄 许可证

本项目仅供学习研究使用，不构成投资建议。

---

**免责声明**: 本工具仅供学习研究使用，不构成投资建议。投资有风险，决策需谨慎。使用本工具进行投资决策的风险由用户自行承担。 