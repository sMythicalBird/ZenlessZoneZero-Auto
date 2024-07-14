@echo off
:main
title ZenlessZoneZero-Auto便捷安装脚本
echo ZenlessZoneZero-Auto便捷安装脚本
echo 请以管理员身份运行
echo 在开始安装之前，请确认已阅读readme
pause
echo 是否安装python3.12.4?(如电脑中有高于此版本的python则不需要安装，如否或版本低于3.10请安装，低版本请卸载)
echo 1.是
echo 2.否
echo 请输入你的选择：
set /p ispython=

if "%ispython%"=="1" goto :installpython
if "%ispython%"=="2" goto :download
goto :inputerror1

:installpython
echo 开始安装！
set url="https://mirrors.huaweicloud.com/python/3.12.4/python-3.12.4-amd64.exe"
set localPath="%temp%\python.exe"

certutil -urlcache -split -f "%url%" "%localPath%"
start /wait "" "%localPath%" /quiet InstallAllUsers=1 PrependPath=1 DefaultAllUsersTargetDir="%ProgramFiles%\Python312"
echo 安装完成！
echo 升级pip中
"%ProgramFiles%\Python312\python" -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
"%ProgramFiles%\Python312\Scripts\pip" install setuptools -i https://mirrors.aliyun.com/pypi/simple
"%ProgramFiles%\Python312\Scripts\pip" config set global.index-url https://mirrors.aliyun.com/pypi/simple
pause
goto :download

:download
echo 正在下载Git中
certutil -urlcache -split -f "https://mirrors.huaweicloud.com/git-for-windows/v2.40.0.windows.1/MinGit-2.40.0-64-bit.zip" "%temp%\git.zip"
set zipFile="%temp%\git.zip"
set extractTo="%temp%\git"
powershell -Command "Expand-Archive '%zipFile%' '%extractTo%'"
mkdir "%ProgramFiles%\ZenlessZoneZero-Auto"
cd /d "%ProgramFiles%\ZenlessZoneZero-Auto"
"%extractTo%\cmd\git.exe" clone https://githubfast.com/sMythicalBird/ZenlessZoneZero-Auto.git
pause
goto :whichversion

:whichversion
cd /d "%ProgramFiles%\ZenlessZoneZero-Auto\ZenlessZoneZero-Auto"
cls
echo 请查看readme,并选择你需要安装的版本
echo 1.CUDA、CuDNN依赖与本项目GPU版本依赖
echo 2.仅安装GPU版本依赖
echo 3.仅安装CPU版本依赖
echo 请选择：
set /p isversion=
if "%isversion%"=="1" goto :installall
if "%isversion%"=="2" goto :installgpu
if "%isversion%"=="3" goto :installcpu
goto :inputerror2

:installall
echo 开始安装！
"%ProgramFiles%\Python312\Scripts\pip" install -r requirements-cuda.txt
"%ProgramFiles%\Python312\Scripts\pip" install -r requirements.txt
echo 安装完成！
goto :end

:installgpu
echo 开始安装！
"%ProgramFiles%\Python312\Scripts\pip" install -r requirements.txt
echo 安装完成！
goto :end

:installcpu
echo 开始安装！
"%ProgramFiles%\Python312\Scripts\pip" install -r requirements-cpu.txt
echo 安装完成！
goto :end

:inputerror1
echo 输入错误，请重新输入
goto :main

:inputerror2
echo 输入错误，请重新输入
goto :whichversion

:end
echo 安装完成，运行请查看readme
pause