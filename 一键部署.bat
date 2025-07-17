@echo off
title BandMaster Pro - 一键部署工具
chcp 65001 >nul

echo.
echo ========================================
echo   BandMaster Pro - 一键部署工具
echo ========================================
echo.

:MENU
echo 请选择部署方案:
echo.
echo 1. 便携式包 (推荐新手)
echo 2. PyInstaller独立程序
echo 3. Docker容器化
echo 4. 源码直接运行
echo 5. 查看部署指南
echo 6. 退出
echo.
set /p choice=请输入选项 (1-6): 

if "%choice%"=="1" goto PORTABLE
if "%choice%"=="2" goto PYINSTALLER  
if "%choice%"=="3" goto DOCKER
if "%choice%"=="4" goto SOURCE
if "%choice%"=="5" goto GUIDE
if "%choice%"=="6" goto EXIT

echo 无效选项，请重新选择
goto MENU

:PORTABLE
echo.
echo 🚀 开始创建便携式包...
python portable_package.py
if %errorlevel% equ 0 (
    echo ✅ 便携式包创建完成!
) else (
    echo ❌ 便携式包创建失败
)
pause
goto MENU

:PYINSTALLER
echo.
echo 🚀 开始PyInstaller打包...
python build_package.py
if %errorlevel% equ 0 (
    echo ✅ PyInstaller打包完成!
) else (
    echo ❌ PyInstaller打包失败
)
pause
goto MENU

:DOCKER
echo.
echo 🚀 开始Docker容器化...
python docker_package.py
if %errorlevel% equ 0 (
    echo ✅ Docker配置文件创建完成!
    echo 💡 请运行 docker_build.bat 构建镜像
) else (
    echo ❌ Docker配置创建失败
)
pause
goto MENU

:SOURCE
echo.
echo 🚀 直接运行源码...
pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo ✅ 依赖安装完成，启动应用...
    streamlit run app.py
) else (
    echo ❌ 依赖安装失败
)
pause
goto MENU

:GUIDE
echo.
echo 📋 打开部署指南...
if exist "DEPLOYMENT_GUIDE.md" (
    start DEPLOYMENT_GUIDE.md
) else (
    echo ❌ 部署指南文件不存在
    echo 💡 请先运行 python deployment_guide.py 创建指南
)
pause
goto MENU

:EXIT
echo.
echo 👋 感谢使用 BandMaster Pro!
exit /b 0
