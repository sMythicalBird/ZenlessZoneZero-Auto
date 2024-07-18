@echo off
@REM 修改编码
chcp 65001
rem 进入当前文件夹
cd /d %~dp0

@REM 输出当前目录
echo 当前目录：%CD%

@REM 判断当前是否以管理员权限运行，如果不是则提示并退出
net session >nul 2>nul
if %errorlevel% neq 0 (
    echo 请以管理员权限运行此脚本。
    pause
    exit /b 1
)

@REM 运行程序
python main.py
pause
exit