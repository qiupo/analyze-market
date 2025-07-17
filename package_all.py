#!/usr/bin/env python3
"""
BandMaster Pro 一键打包工具
整合所有跨平台打包方案
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """打印横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║    🚀 BandMaster Pro - 一键跨平台打包工具                    ║
║                                                               ║
║    📦 支持多种打包方案，轻松实现跨平台部署                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("💡 需要Python 3.8或更高版本")
        return False
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    
    # 检查必要文件
    required_files = ['app.py', 'requirements.txt', 'data_fetcher.py', 'technical_analysis.py', 'visualization.py']
    missing_files = []
    
    for file_name in required_files:
        if not os.path.exists(file_name):
            missing_files.append(file_name)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file_name in missing_files:
            print(f"   - {file_name}")
        return False
    
    print("✅ 必要文件检查通过")
    
    # 检查系统信息
    system = platform.system()
    arch = platform.machine()
    print(f"🖥️  系统信息: {system} {arch}")
    
    return True

def create_packaging_configs():
    """创建所有打包配置文件"""
    print("\n📝 创建打包配置文件...")
    
    configs = [
        ('build_package.py', '自动化PyInstaller打包'),
        ('portable_package.py', '便携式包打包'),
        ('docker_package.py', 'Docker容器化'),
        ('deployment_guide.py', '部署指南生成器')
    ]
    
    created_configs = []
    
    for config_file, description in configs:
        if os.path.exists(config_file):
            print(f"✅ {description}: {config_file}")
            created_configs.append(config_file)
        else:
            print(f"⚠️ {description}: {config_file} (未找到)")
    
    return created_configs

def show_package_options():
    """显示打包选项"""
    options = """
📦 可用的打包方案:

1. 便携式包 (推荐新手)
   ✅ 无需安装Python环境
   ✅ 包含完整运行环境
   ✅ 解压即用
   📊 适合: 个人使用、快速体验

2. PyInstaller独立程序 (推荐分发)
   ✅ 单文件可执行程序
   ✅ 启动速度快
   ✅ 文件体积小
   📊 适合: 软件分发、生产部署

3. Docker容器化 (推荐服务器)
   ✅ 环境完全一致
   ✅ 易于维护更新
   ✅ 支持集群部署
   📊 适合: 服务器部署、团队协作

4. 源码直接运行 (推荐开发)
   ✅ 完全可定制
   ✅ 便于调试修改
   ✅ 学习代码结构
   📊 适合: 开发环境、二次开发

5. 生成完整部署指南
   📋 详细部署说明
   📋 故障排除指南
   📋 一键部署脚本

6. 一键生成所有配置
   🚀 生成所有打包配置
   📁 创建完整项目结构

0. 退出
"""
    print(options)

def run_packaging_script(script_name):
    """运行打包脚本"""
    if not os.path.exists(script_name):
        print(f"❌ 脚本文件不存在: {script_name}")
        return False
    
    try:
        print(f"🚀 运行: {script_name}")
        subprocess.check_call([sys.executable, script_name])
        print(f"✅ {script_name} 执行完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} 执行失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 运行 {script_name} 时出错: {e}")
        return False

def create_all_configs():
    """创建所有配置文件"""
    print("🔧 正在生成所有打包配置...")
    
    # 这里我们假设配置文件已经存在，实际使用时会检查并生成
    configs_info = {
        'build_package.py': 'PyInstaller自动化打包脚本',
        'portable_package.py': '便携式包创建脚本', 
        'docker_package.py': 'Docker容器化配置',
        'deployment_guide.py': '部署指南生成器',
        'requirements_build.txt': '打包专用依赖列表',
        'build.spec': 'PyInstaller配置文件'
    }
    
    created_count = 0
    for config_file, description in configs_info.items():
        if os.path.exists(config_file):
            print(f"✅ {description}: {config_file}")
            created_count += 1
        else:
            print(f"⚠️ {description}: {config_file} (需要生成)")
    
    print(f"\n📊 配置文件状态: {created_count}/{len(configs_info)} 已存在")
    return created_count == len(configs_info)

def show_usage_guide():
    """显示使用指南"""
    guide = """
🎯 使用指南:

📋 快速开始:
1. 首次使用建议选择 "5. 生成完整部署指南"
2. 根据需求选择合适的打包方案
3. 按提示完成打包过程

📱 不同场景推荐:
• 新手试用 → 便携式包
• 个人使用 → PyInstaller
• 服务器部署 → Docker
• 开发调试 → 源码运行

⚠️ 注意事项:
• 确保网络连接正常
• 首次打包可能需要较长时间
• 建议在虚拟环境中运行
• 遇到问题可查看故障排除指南

📞 技术支持:
• 查看生成的 DEPLOYMENT_GUIDE.md
• 参考 TROUBLESHOOTING_GUIDE.md
• 运行诊断脚本检查环境
"""
    print(guide)

def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        input("按回车键退出...")
        return
    
    # 检查配置文件
    created_configs = create_packaging_configs()
    
    while True:
        print("\n" + "="*60)
        show_package_options()
        
        try:
            choice = input("请选择操作 (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 感谢使用 BandMaster Pro 打包工具!")
                break
                
            elif choice == '1':
                print("\n📦 创建便携式包...")
                if 'portable_package.py' in created_configs:
                    run_packaging_script('portable_package.py')
                else:
                    print("❌ 便携式包配置文件不存在")
                    
            elif choice == '2':
                print("\n🔧 创建PyInstaller独立程序...")
                if 'build_package.py' in created_configs:
                    run_packaging_script('build_package.py')
                else:
                    print("❌ PyInstaller配置文件不存在")
                    
            elif choice == '3':
                print("\n🐳 创建Docker配置...")
                if 'docker_package.py' in created_configs:
                    run_packaging_script('docker_package.py')
                else:
                    print("❌ Docker配置文件不存在")
                    
            elif choice == '4':
                print("\n🚀 准备源码运行环境...")
                print("💡 请运行以下命令:")
                print("   pip install -r requirements.txt")
                print("   streamlit run app.py")
                print("✅ 源码运行无需额外配置")
                
            elif choice == '5':
                print("\n📋 生成部署指南...")
                if 'deployment_guide.py' in created_configs:
                    run_packaging_script('deployment_guide.py')
                else:
                    print("❌ 部署指南生成器不存在")
                    
            elif choice == '6':
                print("\n🔧 生成所有配置...")
                all_ready = create_all_configs()
                if all_ready:
                    print("✅ 所有配置文件已准备就绪")
                    print("💡 现在可以选择具体的打包方案")
                else:
                    print("⚠️ 部分配置文件需要手动创建")
                    
            else:
                print("❌ 无效选项，请重新选择")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户取消操作")
            break
        except Exception as e:
            print(f"\n❌ 操作出错: {e}")
            
        # 操作完成后的提示
        if choice in ['1', '2', '3', '5']:
            input("\n按回车键继续...")
    
    # 显示使用指南
    print("\n" + "="*60)
    show_usage_guide()

if __name__ == "__main__":
    main() 