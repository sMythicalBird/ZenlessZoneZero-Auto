@echo off
:main
title ZenlessZoneZero-Auto便捷安装脚本
echo ZenlessZoneZero-Auto便捷安装脚本
echo 请以管理员身份运行
echo 在开始安装之前，请确认已阅读readme
pause
goto :ispythoninstalled

:ispythoninstalled
echo 正在检测python...
setlocal
where python >nul
if %errorlevel% neq 0 (
    echo Python未安装,正在安装...
    goto :installpython
)
endlocal
python --version | findstr /C:"Python" >nul
if %errorlevel% neq 0 (
    echo Python不正确,正在安装...
    goto :installpython
)
for /f "tokens=2 delims= " %%a in ('python --version') do set version=%%a
set major=%version:~0,1%
set minor=%version:~2,2%
if %major% gtr 3 (
    goto :whichversion
) else if %major% equ 3 (
    if %minor% gtr 10 (
        goto :whichversion
    ) else if %minor% equ 10 (
        goto :whichversion
    )
)
goto :error1

:installpython
echo 有些杀毒软件会错误的拦截python安装，请注意。
pause
echo 开始安装！
set url="https://mirrors.huaweicloud.com/python/3.10.2/python-3.10.2-amd64.exe"
set localPath="%temp%\python.exe"

certutil -urlcache -split -f "%url%" "%localPath%"
start /wait "" "%localPath%" /quiet InstallAllUsers=1 PrependPath=1 DefaultAllUsersTargetDir="%ProgramFiles%\Python310"
if exist "%ProgramFiles%\Python310\python.exe" (
    echo 安装完成！
) else (
    echo 安装错误！正在重试中...
    start /wait "" "%localPath%" InstallAllUsers=1 PrependPath=1 SimpleInstall=1 SimpleInstallDescription="点击以安装"
    echo 是否安装成功？如未成功请退出脚本并百度，成功请继续
    pause
)
echo 升级pip中
"%ProgramFiles%\Python310\python" -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
"%ProgramFiles%\Python310\Scripts\pip" install setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
"%ProgramFiles%\Python310\Scripts\pip" config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pause
goto :whichversion

:whichversion
cd /d "%~dp0"
cls
echo 正在检查pip是否存在...
where pip >nul 2>&1
if %errorlevel% equ 0 (
    echo pip 已在PATH中找到，使用默认pip。
    set pip_cmd="pip"
) else (
    echo pip 未在PATH中找到，尝试使用前面安装的pip。
    set pip_cmd="%ProgramFiles%\Python310\Scripts\pip.exe"
)
cls
echo 请查看readme,并选择你需要安装的版本
echo 1.仅安装GPU版本依赖
echo 2.仅安装CPU版本依赖
echo 请选择：
set /p isversion=
if "%isversion%"=="1" goto :installgpu
if "%isversion%"=="2" goto :installcpu
goto :inputerror2


:installgpu
echo 开始安装！
%pip_cmd% install -r requirements.txt
echo 安装完成！
goto :installvc

:installcpu
echo 开始安装！
%pip_cmd% install -r requirements-cpu.txt
echo 安装完成！
goto :installvc

:installvc
cls
echo 安装VC运行库
echo 请注意：安装VC运行库可能需要一段时间，请耐心等待。
certutil -urlcache -split -f "https://aka.ms/vs/17/release/vc_redist.x64.exe" "%temp%\vc.exe"
start /wait "" "%temp%\vc.exe" /install /quiet /norestart
echo 安装完成！
echo 如果启动脚本提示"动态链接库(DLL)初始化例程失败",请重新启动电脑尝试。
echo 如果还是不行，请尝试重新安装onnxruntime。
pause
goto :end

:error1
echo python版本过低！
echo 请完全卸载python后尝试安装。
pause
exit /b

:inputerror2
echo 输入错误，请重新输入
goto :whichversion

:end
cls
echo 安装完成，运行请查看readme
pause