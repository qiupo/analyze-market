#!/usr/bin/env python3
"""
BandMaster Pro 便携式打包方案
创建包含所有依赖的便携式应用包
"""

import os
import sys
import subprocess
import shutil
import zipfile
import platform
from pathlib import Path

def create_virtual_env():
    """创建虚拟环境"""
    print("🔧 创建便携式虚拟环境...")
    
    venv_path = Path('portable_env')
    
    # 清理已存在的环境
    if venv_path.exists():
        shutil.rmtree(venv_path)
    
    # 创建新的虚拟环境
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', str(venv_path)])
        print("✅ 虚拟环境创建成功")
        return venv_path
    except Exception as e:
        print(f"❌ 虚拟环境创建失败: {e}")
        return None

def install_dependencies(venv_path):
    """在虚拟环境中安装依赖"""
    print("📦 安装应用依赖...")
    
    system = platform.system().lower()
    
    if system == 'windows':
        pip_path = venv_path / 'Scripts' / 'pip.exe'
        python_path = venv_path / 'Scripts' / 'python.exe'
    else:
        pip_path = venv_path / 'bin' / 'pip'
        python_path = venv_path / 'bin' / 'python'
    
    try:
        # 升级pip
        subprocess.check_call([str(pip_path), 'install', '--upgrade', 'pip'])
        
        # 安装应用依赖
        subprocess.check_call([str(pip_path), 'install', '-r', 'requirements.txt'])
        
        print("✅ 依赖安装成功")
        return python_path
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        return None

def create_launcher_scripts(venv_path, python_path):
    """创建启动脚本"""
    print("📝 创建便携式启动脚本...")
    
    system = platform.system().lower()
    
    # Windows启动脚本
    if system == 'windows':
        batch_content = f'''@echo off
title BandMaster Pro - 智策波段交易助手
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo   BandMaster Pro - 智策波段交易助手
echo ========================================
echo.
echo 🚀 正在启动应用...
echo 📊 首次启动可能需要10-30秒，请耐心等待
echo.

REM 检查虚拟环境是否存在
if not exist "portable_env\\Scripts\\python.exe" (
    echo ❌ 错误: 找不到Python环境
    echo 💡 请确保所有文件完整
    pause
    exit /b 1
)

REM 启动应用
portable_env\\Scripts\\python.exe -m streamlit run app.py --server.headless=true --browser.gatherUsageStats=false

if %errorlevel% neq 0 (
    echo.
    echo ❌ 应用启动失败
    echo 💡 可能的解决方案:
    echo    1. 检查网络连接
    echo    2. 确保端口8501未被占用
    echo    3. 以管理员权限运行
    pause
)
'''
        
        with open('启动应用.bat', 'w', encoding='gbk') as f:
            f.write(batch_content)
    
    # Unix系统启动脚本
    shell_content = f'''#!/bin/bash

echo "========================================"
echo "  BandMaster Pro - 智策波段交易助手"
echo "========================================"
echo
echo "🚀 正在启动应用..."
echo "📊 首次启动可能需要10-30秒，请耐心等待"
echo

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查虚拟环境
if [ ! -f "portable_env/bin/python" ]; then
    echo "❌ 错误: 找不到Python环境"
    echo "💡 请确保所有文件完整"
    exit 1
fi

# 启动应用
portable_env/bin/python -m streamlit run app.py --server.headless=true --browser.gatherUsageStats=false

if [ $? -ne 0 ]; then
    echo
    echo "❌ 应用启动失败"
    echo "💡 可能的解决方案:"
    echo "   1. 检查网络连接"
    echo "   2. 确保端口8501未被占用"
    echo "   3. 检查文件权限"
    read -p "按回车键退出..."
fi
'''
    
    with open('启动应用.sh', 'w', encoding='utf-8') as f:
        f.write(shell_content)
    
    # 设置执行权限
    if system != 'windows':
        os.chmod('启动应用.sh', 0o755)
    
    print("✅ 启动脚本创建完成")

def create_install_script():
    """创建安装脚本"""
    print("📝 创建安装脚本...")
    
    install_content = '''#!/usr/bin/env python3
"""
BandMaster Pro 便携式安装脚本
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True

def install_packages():
    """安装必要的包"""
    packages = ['venv', 'pip']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            return False
    
    return True

def main():
    print("🚀 BandMaster Pro 便携式安装程序")
    print("=" * 50)
    
    # 检查Python环境
    if not check_python():
        input("按回车键退出...")
        return
    
    if not install_packages():
        print("❌ 系统环境检查失败")
        input("按回车键退出...")
        return
    
    print("✅ 系统环境检查通过")
    print("💡 请运行 portable_package.py 创建便携式包")

if __name__ == "__main__":
    main()
'''
    
    with open('install.py', 'w', encoding='utf-8') as f:
        f.write(install_content)
    
    print("✅ 安装脚本创建完成")

def create_portable_readme():
    """创建便携式包说明"""
    readme_content = '''# BandMaster Pro - 便携式版本

## 📦 便携式包说明

这是BandMaster Pro的便携式版本，包含完整的Python环境和所有依赖，可以在没有Python环境的系统上直接运行。

## 📂 目录结构

```
BandMaster-Pro-Portable/
├── app.py                    # 主应用文件
├── data_fetcher.py          # 数据获取模块
├── technical_analysis.py    # 技术分析模块
├── visualization.py         # 可视化模块
├── config.py               # 配置文件
├── requirements.txt        # 依赖列表
├── portable_env/           # 便携式Python环境
├── 启动应用.bat           # Windows启动脚本
├── 启动应用.sh            # Linux/macOS启动脚本
├── logs/                   # 日志目录
└── README.md              # 说明文档
```

## 🚀 使用方法

### Windows系统
1. 双击 `启动应用.bat`
2. 等待应用启动（首次可能需要30秒）
3. 浏览器自动打开应用界面

### macOS/Linux系统
1. 打开终端，进入应用目录
2. 运行: `./启动应用.sh`
3. 等待应用启动
4. 浏览器自动打开应用界面

## 🔧 功能特色

- **完全便携**: 无需安装Python环境
- **依赖隔离**: 不影响系统Python环境
- **跨平台**: 支持Windows、macOS、Linux
- **即开即用**: 双击启动，简单易用

## 📊 系统要求

### 最低配置
- **操作系统**: Windows 10/macOS 10.14/Ubuntu 18.04
- **内存**: 4GB RAM
- **硬盘**: 500MB可用空间
- **网络**: 需要网络连接获取数据

### 推荐配置
- **操作系统**: Windows 11/macOS 12+/Ubuntu 20.04+
- **内存**: 8GB RAM
- **硬盘**: 1GB可用空间
- **网络**: 稳定的网络连接

## ⚡ 性能优化

1. **首次启动**: 可能需要较长时间加载
2. **缓存机制**: 重复使用会更快
3. **内存管理**: 自动清理无用缓存
4. **网络优化**: 智能重试机制

## 🛠️ 故障排除

### 常见问题

**Q: 双击启动脚本没有反应？**
A: 
- Windows: 右键选择"以管理员身份运行"
- macOS/Linux: 终端运行 `chmod +x 启动应用.sh`

**Q: 提示端口被占用？**
A: 
- 关闭其他可能占用8501端口的程序
- 重启计算机后再试

**Q: 无法获取股票数据？**
A:
- 检查网络连接
- 确认股票代码格式正确（6位数字）
- 稍后重试

**Q: 启动很慢？**
A:
- 首次启动需要初始化，属正常现象
- 后续启动会显著加快
- 确保有足够的磁盘空间

### 日志查看

如果遇到问题，可查看 `logs/` 目录下的日志文件：
- `app.log` - 应用日志
- `error.log` - 错误日志

## 🔄 更新升级

1. 下载新版便携式包
2. 备份 `logs/` 目录（可选）
3. 替换所有文件
4. 重新启动应用

## 📞 技术支持

### 自检清单
- [ ] 检查系统兼容性
- [ ] 确认网络连接正常
- [ ] 验证磁盘空间充足
- [ ] 尝试以管理员权限运行

### 联系方式
如果问题仍未解决，请提供以下信息：
- 操作系统版本
- 错误截图
- 日志文件内容

## ⚠️ 重要提示

1. **数据安全**: 本地运行，数据不会上传
2. **网络连接**: 仅用于获取公开股票数据
3. **投资风险**: 分析结果仅供参考，投资需谨慎
4. **版权声明**: 仅供学习研究使用

---

**免责声明**: 本工具提供的分析结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。
'''
    
    with open('Portable_README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ 便携式包说明创建完成")

def create_package_archive(venv_path):
    """创建便携式包压缩文件"""
    print("📦 创建便携式包压缩文件...")
    
    # 要包含的文件和目录
    include_files = [
        'app.py',
        'data_fetcher.py', 
        'technical_analysis.py',
        'visualization.py',
        'config.py',
        'requirements.txt',
        '启动应用.bat',
        '启动应用.sh',
        'Portable_README.md'
    ]
    
    include_dirs = [
        str(venv_path),
        'logs'
    ]
    
    # 创建logs目录（如果不存在）
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    archive_name = f"BandMaster-Pro-Portable-{platform.system()}-{platform.machine()}.zip"
    
    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加文件
            for file_name in include_files:
                if os.path.exists(file_name):
                    zipf.write(file_name, file_name)
                    print(f"   添加文件: {file_name}")
            
            # 添加目录
            for dir_name in include_dirs:
                dir_path = Path(dir_name)
                if dir_path.exists():
                    for file_path in dir_path.rglob('*'):
                        if file_path.is_file():
                            arcname = str(file_path)
                            zipf.write(file_path, arcname)
                    print(f"   添加目录: {dir_name}")
        
        file_size = os.path.getsize(archive_name) / (1024 * 1024)  # MB
        print(f"✅ 便携式包创建成功: {archive_name} ({file_size:.1f} MB)")
        return archive_name
        
    except Exception as e:
        print(f"❌ 创建便携式包失败: {e}")
        return None

def main():
    """主函数"""
    print("📦 BandMaster Pro 便携式打包工具")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ['app.py', 'requirements.txt']
    for file_name in required_files:
        if not os.path.exists(file_name):
            print(f"❌ 缺少必要文件: {file_name}")
            return
    
    print("✅ 必要文件检查通过")
    
    # 创建虚拟环境
    venv_path = create_virtual_env()
    if not venv_path:
        return
    
    # 安装依赖
    python_path = install_dependencies(venv_path)
    if not python_path:
        return
    
    # 创建启动脚本
    create_launcher_scripts(venv_path, python_path)
    
    # 创建安装脚本
    create_install_script()
    
    # 创建说明文档
    create_portable_readme()
    
    # 创建压缩包
    archive_name = create_package_archive(venv_path)
    
    print("\n" + "=" * 50)
    print("🎉 便携式打包完成!")
    
    if archive_name:
        print(f"📦 便携式包: {archive_name}")
        print("📋 使用说明: Portable_README.md")
    
    print("🚀 快速测试:")
    print("   1. 运行启动脚本测试应用")
    print("   2. 解压便携式包到其他位置测试")
    print("=" * 50)

if __name__ == "__main__":
    main() 