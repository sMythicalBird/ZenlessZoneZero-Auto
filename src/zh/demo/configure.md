---
title: 高级设置
icon: sliders
order: 2
category:
  - 使用指南
tag:
  - 高级设置
---

::: warning
本文内容更偏向于对电脑有一定基础的用户，如果您是电脑小白。建议直接使用 [快速开始](deploy.md) 的教程，此处为高级选项。对于体验有一定改善
:::

## 1 使用 Conda 环境

### 1.1 下载本项目

```bash
git clone https://github.com/sMythicalBird/ZenlessZoneZero-Auto.git
cd ZenlessZoneZero-Auto
```
::: warning
`GPU 版本` 和 `CPU 版本` 二选一，`GPU 版本` 使用前提是你的电脑上使用的是 NVIDIA 显卡
:::
### 1.2 安装 Conda

`Conda` 分为 `Anaconda` 和 `Miniconda`，`Anaconda` 是一个包含了许多常用库的集合版本，`Miniconda` 是精简版本，我们这里使用 [Miniconda](https://docs.anaconda.com/miniconda/)

![Conda](/image/Conda.png)

检查是否安装成功

```bash
conda --version
```

### 1.3 创建 Conda 环境

1. 打开 `Anaconda Prompt`
2. 设置镜像源

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

3. 创建环境（`Python 3.10`）

```bash
conda create -n py310 python=3.10
```

4. 查看环境
```bash
conda env list
```

5. 激活环境
```bash
conda activate py310
```

### 1.4 安装相关依赖

#### 1.4.1 GPU 版本

1. 安装 `Cudatookit` 和 `Cundnn`

安装 `Cudatookit 11.8`

```bash
conda install cudatoolkit=11.8
```

安装 `Cudnn 8.9.7.29`

```bash
conda install cudnn=8.9.7.29
```

2. 安装 GPU 相关依赖

`pip` 配置镜像源

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

切换到项目目录下安装依赖

```bash
pip install -r requirements-dml.txt
```

#### 1.4.2 CPU 版本

`CPU 版本` 不需要安装 `Cudatoolkit` 和 `Cudnn`

1. 安装 CPU 相关依赖

`pip` 配置镜像源

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

切换到项目目录下安装依赖

```bash
pip install -r requirements-cpu.txt
```

### 1.5 注意事项

1. GPU、CPU 二选一
2. GPU 安装 `Cudatoolkit` 和 `Cudnn` 严格按照教程来，使用其他版本出现问题 **概不负责**
3. 安装结束后就可以用 `Conda` 中的环境变量运行脚本了
```bash
python main.py
```
4、如果电脑在此教程之前已经安装过 `CUDA`，且运行脚本时出现以下错误
```bash
ImportError: DLL load failed while importing onnxruntime_pybind_state: 动态链接库（DLL）初始化例程失败
```
请运行下列指令
```bash
pip uninstall onnxruntime-gpu
pip install onnxruntime-gpu==1.17
```
## 2 后台运行

### 2.1 创建用户

1. 打开 `文件资源管理器`，右键此电脑，点击管理，打开 `计算机管理` 界面
::: center
![打开计算机管理](/image/computermanager.png)
:::

2. 打开 `本地用户和组`，右键用户，右键菜单选择 `新用户`

![打开用户组](/image/user.png)

3. 创建新用户

![新建用户](/image/createuser.png)

4. 添加远程桌面用户，打开远程桌面，点击远程桌面用户，点击添加，将刚才新建的用户添加进去

![添加用户](/image/adduser.png)

### 2.2 配置本地组策略

1. `Windows + R` 打开运行窗口，输入 `gpedit.msc`，打开 `本地组策略编辑器，如图示点击
::: center
![运行组策略](/image/rungpedit.png)
:::

2. 按图示点击窗口

::: center
![点击窗口](/image/gpeditclick1.png)
:::

::: center
![点击窗口](/image/gpeditclick2.png)
:::

::: tip 选择以下三项配置进行修改
1. 启用 `允许用户通过远程桌面服务进行远程连接`

![启用功能](/image/allow1.png)

2. 启用 `限制连接的数量`，`允许的 RD 最大连接数` 视情况而定

![启用功能](/image/allow2.png)

3. 启用 `将远程桌面服务用户限制到单独的远程桌面服务会话`

![启用功能](/image/allow3.png)
:::

### 2.3 安装 `RDPWrap` 补丁

[下载 RDPWrap](https://github.com/stascorp/rdpwrap/releases)，解压后包含以下文件，右键 `install.bat` 后选择 `以管理员身份运行`。此时会自动安装补丁

::: center
![RDPWrap](/image/RDPWrapInstall.png)
:::

安装后以管理员身份运行 `RDPConf.exe` 查看支持情况，如果全绿就完成了（一般会有个别冒红）

::: center
![RDPWrap](/image/RDPWrapCheck.png)
:::

如果显示 `Wrapper State` 显示未安装或者显示有 `[not supported]` 说明补丁的配置文件没有此时电脑对应的版本配置，我们需要更新配置文件

首先以管理员身份打开 `cmd`，输入以下命令停掉 `termservice`

```bash
net stop termservice
```

然后使用文本编辑器打开 `C:\Program Files\RDP Wrapper\rdpwrap.ini` 配置文件，将 [rdpwrap.ini](https://github.com/sebaxakerhtc/rdpwrap.ini/blob/master/rdpwrap.ini) 里面的内容复制到上述配置文件 `rdpwrap.ini` 里

::: center
![停止服务](/image/stopservice.png)
:::

替换完成以后保存文件，此时继续在 `cmd` 里输入 `net start termservice` 启动 `termservice`

::: center
![启动服务](/image/runservice.png)
:::

此时重新打开 `RDPConf.exe` 文件就应该是全绿的了

如果仍然有红色错误，则进入上述补丁解压后的文件夹，打开终端，输入如下命令重启服务

```bash
.\RDPWInst.exe -r
```

::: tip 提示
如果还是不行，请重启电脑后再次检查
:::

### 2.4 连接本地桌面

如果上述所有操作都没有问题的话，就可以本地远程连接本地桌面了

打开 `远程桌面连接`，输入 `本地回环地址`，例如 `127.0.0.2`
:::center
![成功连接](/image/succesconnect.png)
:::
::: caution 警告
不要使用 `127.0.0.1`，否则会报以下错误
:::center
![运行错误](/image/wrong.png)
:::

选择刚才新建的用户，输入密码，连接到远程客户端

:::center
![选择用户](/image/ChooseUser.png)
:::

### 2.5 启动游戏

因为安装游戏的用户不是远程连接使用的的用户，所以远程桌面的应用里是没有米哈游启动器和绝区零的

直接打开游戏所在目录，找到 `ZenlessZoneZero.exe` 该程序，双击启动

![启动游戏](/image/rungame.png)

### 2.6 启动脚本

详见 [快速开始](deploy.md)