---
title: Settings
icon: sliders
order: 2
category:
  - Use guide
tag:
  - Settings
---

::: warning
The content of this article is more based on users who have a certain foundation for a computer, If you don't understand the computer. It is recommended to directly use the tutorial to [Quick Start](deploy.md). Here is a high-level option. Some improvement of experience
:::

## 1 Use Conda Environment

### 1.1 Download Project

```bash
git clone https://github.com/sMythicalBird/ZenlessZoneZero-Auto.git
cd ZenlessZoneZero-Auto
```
::: warning
`GPU Version` And `cpu version` choice one，`GPU version` premise that you use the NVIDIA graphics card on your computer
:::
### 1.2 Install Conda

`Conda` Divided into `Anaconda` and `Miniconda`, `Anaconda` is a collection version containing many commonly used libraries. [Miniconda](https://docs.anaconda.com/miniconda/)

![Conda](/image/Conda.png)

Check whether the installation is successful

```bash
conda --version
```

### 1.3 Create Conda Environment

1. Open `Anaconda Prompt`
2. Set the mirror source

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

3. Create an environment（`Python 3.10`）

```bash
conda create -n py310 python=3.10
```

4. Look at the environment
```bash
conda env list
```

5. Active environment
```bash
conda activate py310
```

### 1.4 Installation related dependencies

#### 1.4.1 GPU Version

1. Install `Cudatookit` and `Cundnn`

Install `Cudatookit 11.8`

```bash
conda install cudatoolkit=11.8
```

Install `Cudnn 8.9.7.29`

```bash
conda install cudnn=8.9.7.29
```

2. Install GPU-related dependencies

`pip` Configuration mirror source

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

Switch to the project directory installation dependencies

```bash
pip install -r requirements-dml.txt
```

#### 1.4.2 CPU Version

`CPU Version` doesn't need install `Cudatoolkit` and `Cudnn`

1. Install CPU -related dependencies

`pip` Configuration mirror source

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

Switch to the project directory installation dependencies

```bash
pip install -r requirements-cpu.txt
```

### 1.5 Precautions

1. GPU, CPU Two Select One
2. The GPU installation `CUDATOOLKIT` and `CUDNN` strictly follow the tutorial, using other versions problems **are not responsible for**
3. After the installation, you can run the script with the environment variable in the `Conda`
```bash
python main.py
```
4、If the computer has been installed before this tutorial, the following errors appear when running the script
```bash
ImportError: DLL load failed while importing onnxruntime_pybind_state: 动态链接库（DLL）初始化例程失败
```
Please run the following instructions
```bash
pip uninstall onnxruntime-gpu
pip install onnxruntime-gpu==1.17
```
## 2 Background operation

### 2.1 Create users

1. Open the `explorer`, right -click this computer, click the management, open the `computer management` interface
::: center
![打开计算机管理](/image/computermanager.png)
:::

1. Open the 'local user and group', right-click the `user`, right-click `menu` and `select new users`

![打开用户组](/image/user.png)

3. Create a new user

![新建用户](/image/createuser.png)

4. Add remote desktop users, turn on the remote desktop, click on remote desktop users, click to add, add the newly built users in

![添加用户](/image/adduser.png)

### 2.2 Configure local group strategy

1. `Windows + R` Open the running window, enter the `gpedit.msc`, open the local group strategy editor, as shown in the figure, click on
::: center
![运行组策略](/image/rungpedit.png)
:::

2. Click the window according to the figure

::: center
![点击窗口](/image/gpeditclick1.png)
:::

::: center
![点击窗口](/image/gpeditclick2.png)
:::

::: tip Select the following three configurations to modify
1. Enable `Allow users to remotely connect through remote desktop services`

![启用功能](/image/allow1.png)

2. Enable the `number of connections to limit the number of connections`, `The maximum number of RD connections allowed` to depend on the situation

![启用功能](/image/allow2.png)

3. Enable `to limit the remote desktop service users to a separate remote desktop service session`

![启用功能](/image/allow3.png)
:::

### 2.3Install `RDPWRAP` Patch

[Downlaod RDPWrap](https://github.com/stascorp/rdpwrap/releases)，After decompression, it contains the following files. After right-click `Install.bat`, select `Run as an administrator`. At this time, the patch will be automatically installed

::: center
![RDPWrap](/image/RDPWrapInstall.png)
:::

After installation, run as an administrator `rdpconf.exe` to view the support situation.

::: center
![RDPWrap](/image/RDPWrapCheck.png)
:::

If the display `Wrapper Sate` shows the uncomfortable or displayed `[not supported]` The configuration file of the patch does not have the corresponding version configuration at this time, we need to update the configuration file

First open `cmd` as an administrator, enter the following commands to stop `termservice`

```bash
net stop termservice
```

Then use the text editor to open the `C:\Program Files\RDPWrapper\rdpwrap.ini` Configuration file, copy the content in the [rdpwrap.ini](https://github.com/sebaxakerhtc/rdpwrap.ini/blob/master/rdpwrap.ini) to the above configuration file` rdpwrap.ini`

::: center
![停止服务](/image/stopservice.png)
:::

Save the file after replacement, and continue to enter the `net start termService` in `cmd` at this time

::: center
![启动服务](/image/runservice.png)
:::

At this time, reopen the `rdpconf.exe` file should be all green

If there is still a red error, enter the folder after the patch decompressing, open the terminal, and enter the following command to restart the service

```bash
.\RDPWInst.exe -r
```

::: tip tip
If it still doesn't work, please restart the computer and check again
:::

### 2.4 Connect the local desktop

If there is no problem with all the above operations, you can remotely connect to the local desktop locally.

Open the remote desktop connection, `enter the local loop address`, such as `127.0.0.2`
:::center
![成功连接](/image/succesconnect.png)
:::
::: caution caution
Not to use `127.0.0.1`, Otherwise, the following errors will be reported
:::center
![运行错误](/image/wrong.png)
:::

Select the newly -built user, enter the password, connect to the remote client

:::center
![选择用户](/image/ChooseUser.png)
:::

### 2.5 Start the game

Because users who install games are not users used remote connection, there are no Mihayou promoters and Zero zero in the application of remote desktop.

Open the directory where the game is located, find the program of `Zenless Zone Zero.exe`, double -click to start

![启动游戏](/image/rungame.png)

### 2.6 Use Script

Read [Quick Start](deploy.md)