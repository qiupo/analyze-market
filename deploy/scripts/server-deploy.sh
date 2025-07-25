#!/bin/bash

# 服务器部署脚本
# Server Deployment Script for Cloud Servers

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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
    echo -e "${BLUE}  服务器部署脚本${NC}"
    echo -e "${BLUE}  Server Deployment Script${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "检测到root用户，建议使用普通用户运行"
        read -p "是否继续? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 更新系统
update_system() {
    print_message "更新系统包..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get upgrade -y
    elif command -v yum &> /dev/null; then
        sudo yum update -y
    elif command -v dnf &> /dev/null; then
        sudo dnf update -y
    else
        print_warning "未知的包管理器"
    fi
}

# 安装基础依赖
install_dependencies() {
    print_message "安装基础依赖..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y \
            python3 \
            python3-pip \
            python3-venv \
            curl \
            wget \
            git \
            build-essential \
            libssl-dev \
            libffi-dev \
            python3-dev \
            libta-lib-dev \
            pkg-config
    elif command -v yum &> /dev/null; then
        sudo yum install -y \
            python3 \
            python3-pip \
            curl \
            wget \
            git \
            gcc \
            openssl-devel \
            libffi-devel \
            python3-devel \
            ta-lib-devel \
            pkgconfig
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y \
            python3 \
            python3-pip \
            curl \
            wget \
            git \
            gcc \
            openssl-devel \
            libffi-devel \
            python3-devel \
            ta-lib-devel \
            pkgconfig
    fi
}

# 安装TA-Lib（如果系统包管理器没有提供）
install_talib_from_source() {
    print_message "检查TA-Lib安装..."
    
    if python3 -c "import talib" 2>/dev/null; then
        print_message "TA-Lib已安装"
        return
    fi
    
    print_message "从源码安装TA-Lib..."
    
    # 下载并编译TA-Lib
    cd /tmp
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
    tar -xzf ta-lib-0.4.0-src.tar.gz
    cd ta-lib/
    ./configure --prefix=/usr/local
    make
    sudo make install
    
    # 更新库路径
    echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
    
    # 清理临时文件
    cd /
    rm -rf /tmp/ta-lib*
    
    print_message "TA-Lib安装完成"
}



# 配置防火墙
configure_firewall() {
    print_message "配置防火墙..."
    
    if command -v ufw &> /dev/null; then
        sudo ufw allow 22/tcp
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        sudo ufw allow 8501/tcp
        sudo ufw --force enable
    elif command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --permanent --add-service=ssh
        sudo firewall-cmd --permanent --add-service=http
        sudo firewall-cmd --permanent --add-service=https
        sudo firewall-cmd --permanent --add-port=8501/tcp
        sudo firewall-cmd --reload
    fi
}

# 创建应用目录
create_app_directory() {
    print_message "创建应用目录..."
    
    sudo mkdir -p /opt/stock-analyzer
    sudo chown $USER:$USER /opt/stock-analyzer
    
    # 复制应用文件
    cp -r . /opt/stock-analyzer/
    cd /opt/stock-analyzer
}

# 部署应用
deploy_application() {
    print_message "部署应用..."
    
    # 给部署脚本执行权限
    chmod +x deploy.sh
    
    # 运行部署脚本
    ./deploy.sh
}

# 配置systemd服务
setup_systemd() {
    print_message "配置systemd服务..."
    
    # 创建服务用户
    sudo useradd -r -s /bin/false stock-analyzer || true
    
    # 复制服务文件
    sudo cp systemd.service /etc/systemd/system/stock-analyzer.service
    
    # 重新加载systemd
    sudo systemctl daemon-reload
    
    # 启用服务
    sudo systemctl enable stock-analyzer.service
    
    print_message "systemd服务配置完成"
}

# 配置Nginx
setup_nginx() {
    print_message "配置Nginx..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y nginx
    elif command -v yum &> /dev/null; then
        sudo yum install -y nginx
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y nginx
    fi
    
    # 复制nginx配置
    sudo cp nginx.conf /etc/nginx/nginx.conf
    
    # 启动nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    
    print_message "Nginx配置完成"
}

# 显示部署结果
show_deployment_result() {
    echo ""
    print_message "部署完成！"
    echo ""
    echo -e "${BLUE}访问信息:${NC}"
    echo "  本地访问: http://localhost:8501"
    echo "  公网访问: http://$(curl -s ifconfig.me):8501"
    echo ""
    echo -e "${BLUE}管理命令:${NC}"
    echo "  启动服务: sudo systemctl start stock-analyzer"
    echo "  停止服务: sudo systemctl stop stock-analyzer"
    echo "  重启服务: sudo systemctl restart stock-analyzer"
    echo "  查看状态: sudo systemctl status stock-analyzer"
    echo "  查看日志: sudo journalctl -u stock-analyzer -f"
    echo ""

    echo ""
    echo -e "${BLUE}TA-Lib验证:${NC}"
    echo "  验证安装: python3 -c 'import talib; print(\"TA-Lib版本:\", talib.__version__)'"
    echo ""
    echo -e "${BLUE}防火墙状态:${NC}"
    if command -v ufw &> /dev/null; then
        sudo ufw status
    elif command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --list-all
    fi
}

# 主函数
main() {
    print_header
    
    # 检查root权限
    check_root
    
    # 更新系统
    update_system
    
    # 安装依赖
    install_dependencies
    
    # 安装TA-Lib
    install_talib_from_source
    

    
    # 配置防火墙
    configure_firewall
    
    # 创建应用目录
    create_app_directory
    
    # 部署应用
    deploy_application
    
    # 配置systemd服务
    setup_systemd
    
    # 配置Nginx
    setup_nginx
    
    # 显示结果
    show_deployment_result
}

# 运行主函数
main "$@" 