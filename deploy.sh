#!/bin/bash

# 智策波段交易助手一键部署脚本
# BandMaster Pro One-Click Deployment Script

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  智策波段交易助手部署脚本${NC}"
    echo -e "${BLUE}  BandMaster Pro Deployment${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查系统要求
check_system_requirements() {
    print_message "检查系统要求..."
    
    # 检查操作系统
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_message "检测到 Linux 系统"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_message "检测到 macOS 系统"
    else
        print_warning "未知操作系统: $OSTYPE"
    fi
    
    # 检查Python版本
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_message "Python版本: $PYTHON_VERSION"
    else
        print_error "未找到Python3，请先安装Python 3.8+"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        print_message "pip3 已安装"
    else
        print_error "未找到pip3，请先安装pip"
        exit 1
    fi
}

# 检查Docker
check_docker() {
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_message "Docker版本: $DOCKER_VERSION"
        return 0
    else
        print_warning "Docker未安装"
        return 1
    fi
}

# 检查Docker Compose
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
        print_message "Docker Compose版本: $COMPOSE_VERSION"
        return 0
    else
        print_warning "Docker Compose未安装"
        return 1
    fi
}

# 传统部署方式
deploy_traditional() {
    print_message "使用传统方式部署..."
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        print_message "创建Python虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    print_message "激活虚拟环境..."
    source venv/bin/activate
    
    # 升级pip
    print_message "升级pip..."
    pip install --upgrade pip
    
    # 安装依赖
    print_message "安装Python依赖..."
    pip install -r requirements.txt
    
    # 创建日志目录
    mkdir -p logs
    
    print_message "传统部署完成！"
    print_message "启动命令: source venv/bin/activate && python start.py"
}

# Docker部署方式
deploy_docker() {
    print_message "使用Docker方式部署..."
    
    # 构建镜像
    print_message "构建Docker镜像..."
    docker build -t stock-analyzer .
    
    # 启动容器
    print_message "启动Docker容器..."
    docker-compose up -d
    
    # 等待服务启动
    print_message "等待服务启动..."
    sleep 10
    
    # 检查服务状态
    if docker-compose ps | grep -q "Up"; then
        print_message "Docker部署成功！"
    else
        print_error "Docker部署失败，请检查日志"
        docker-compose logs
        exit 1
    fi
}

# 显示部署信息
show_deployment_info() {
    echo ""
    print_message "部署完成！"
    echo ""
    echo -e "${BLUE}访问信息:${NC}"
    echo "  本地访问: http://localhost:8501"
    echo "  局域网访问: http://$(hostname -I | awk '{print $1}'):8501"
    echo ""
    echo -e "${BLUE}管理命令:${NC}"
    if [ "$DEPLOY_METHOD" = "docker" ]; then
        echo "  查看日志: docker-compose logs -f"
        echo "  停止服务: docker-compose down"
        echo "  重启服务: docker-compose restart"
        echo "  更新服务: docker-compose pull && docker-compose up -d"
    else
        echo "  启动服务: source venv/bin/activate && python start.py"
        echo "  停止服务: Ctrl+C"
        echo "  更新依赖: source venv/bin/activate && pip install -r requirements.txt --upgrade"
    fi
    echo ""
    echo -e "${BLUE}使用说明:${NC}"
    echo "  1. 在左侧输入股票代码（如：000001）"
    echo "  2. 选择分析周期"
    echo "  3. 点击'开始分析'按钮"
    echo "  4. 查看分析结果"
    echo ""
    echo -e "${YELLOW}⚠️  风险提示: 本系统仅供参考，投资有风险${NC}"
}

# 主函数
main() {
    print_header
    
    # 检查系统要求
    check_system_requirements
    
    # 检查Docker
    DOCKER_AVAILABLE=false
    if check_docker && check_docker_compose; then
        DOCKER_AVAILABLE=true
    fi
    
    # 选择部署方式
    echo ""
    if [ "$DOCKER_AVAILABLE" = true ]; then
        echo "请选择部署方式:"
        echo "1) Docker部署 (推荐)"
        echo "2) 传统部署"
        echo ""
        read -p "请输入选择 (1-2): " choice
        
        case $choice in
            1)
                DEPLOY_METHOD="docker"
                deploy_docker
                ;;
            2)
                DEPLOY_METHOD="traditional"
                deploy_traditional
                ;;
            *)
                print_error "无效选择"
                exit 1
                ;;
        esac
    else
        print_warning "Docker不可用，使用传统部署方式"
        DEPLOY_METHOD="traditional"
        deploy_traditional
    fi
    
    # 显示部署信息
    show_deployment_info
}

# 运行主函数
main "$@" 