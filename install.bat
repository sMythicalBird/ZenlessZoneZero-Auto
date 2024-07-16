@echo off
:main
title ZenlessZoneZero-Auto��ݰ�װ�ű�
echo ZenlessZoneZero-Auto��ݰ�װ�ű�
echo ���Թ���Ա�������
echo �ڿ�ʼ��װ֮ǰ����ȷ�����Ķ�readme
pause
goto :ispythoninstalled

:ispythoninstalled
echo ���ڼ��python...
setlocal
where python >nul
if %errorlevel% neq 0 (
    echo Pythonδ��װ,���ڰ�װ...
    goto :installpython
)
endlocal
python --version | findstr /C:"Python" >nul
if %errorlevel% neq 0 (
    echo Python����ȷ,���ڰ�װ...
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
echo ��Щɱ���������������python��װ����ע�⡣
pause
echo ��ʼ��װ��
set url="https://mirrors.huaweicloud.com/python/3.10.2/python-3.10.2-amd64.exe"
set localPath="%temp%\python.exe"

certutil -urlcache -split -f "%url%" "%localPath%"
start /wait "" "%localPath%" /quiet InstallAllUsers=1 PrependPath=1 DefaultAllUsersTargetDir="%ProgramFiles%\Python310"
if exist "%ProgramFiles%\Python310\python.exe" (
    echo ��װ��ɣ�
) else (
    echo ��װ��������������...
    start /wait "" "%localPath%" InstallAllUsers=1 PrependPath=1 SimpleInstall=1 SimpleInstallDescription="����԰�װ"
    echo �Ƿ�װ�ɹ�����δ�ɹ����˳��ű����ٶȣ��ɹ������
    pause
)
echo ����pip��
"%ProgramFiles%\Python310\python" -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
"%ProgramFiles%\Python310\Scripts\pip" install setuptools -i https://mirrors.aliyun.com/pypi/simple
"%ProgramFiles%\Python310\Scripts\pip" config set global.index-url https://mirrors.aliyun.com/pypi/simple
pause
goto :whichversion

:whichversion
cd /d "%~dp0"
cls
echo ���ڼ��pip�Ƿ����...
where pip >nul 2>&1
if %errorlevel% equ 0 (
    echo pip ����PATH���ҵ���ʹ��Ĭ��pip��
    set pip_cmd="pip"
) else (
    echo pip δ��PATH���ҵ�������ʹ��ǰ�氲װ��pip��
    set pip_cmd="%ProgramFiles%\Python310\Scripts\pip.exe"
)
cls
echo ��鿴readme,��ѡ������Ҫ��װ�İ汾
echo 1.CUDA��CuDNN�����뱾��ĿGPU�汾����
echo 2.����װGPU�汾����
echo 3.����װCPU�汾����
echo ��ѡ��
set /p isversion=
if "%isversion%"=="1" goto :installall
if "%isversion%"=="2" goto :installgpu
if "%isversion%"=="3" goto :installcpu
goto :inputerror2

:installall
echo ��ʼ��װ��
%pip_cmd% install -r requirements-cuda.txt
%pip_cmd% install -r requirements.txt
echo ��װ��ɣ�
goto :installvc

:installgpu
echo ��ʼ��װ��
%pip_cmd% install -r requirements.txt
echo ��װ��ɣ�
goto :installvc

:installcpu
echo ��ʼ��װ��
%pip_cmd% install -r requirements-cpu.txt
echo ��װ��ɣ�
goto :installvc

:installvc
cls
echo ��װVC���п�
echo ��ע�⣺��װVC���п������Ҫһ��ʱ�䣬�����ĵȴ���
certutil -urlcache -split -f "https://aka.ms/vs/17/release/vc_redist.x64.exe" "%temp%\vc.exe"
start /wait "" "%temp%\vc.exe" /install /quiet /norestart
echo ��װ��ɣ�
echo ��������ű���ʾ"��̬���ӿ�(DLL)��ʼ������ʧ��",�������������Գ��ԡ�
echo ������ǲ��У��볢�����°�װonnxruntime��
pause
goto :end

:error1
echo python�汾���ͣ�
echo ����ȫж��python���԰�װ��
pause
exit /b

:inputerror2
echo �����������������
goto :whichversion

:end
cls
echo ��װ��ɣ�������鿴readme
pause