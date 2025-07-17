#!/bin/bash

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
