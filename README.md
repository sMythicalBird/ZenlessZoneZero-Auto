#  绝区零 自动化框架 零号空洞

> 当前项目处于开发阶段，正在开发零号空洞的自动化操作，可能会有很多问题，欢迎大家提出PR，一起完善这个项目。


## 项目简介
绝区零 零号空洞自动化框架是一个基于`Python3.10`的自动化框架

本项目基于图像识别，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。本项目的当前目标是可以让玩家从每周长时间的零号空洞材料刷取中解放出来，只需要在电脑上挂着就可以自动完成。本项目后续也会继续考虑增加其他自动化操作，帮助玩家做到日常托管。

本项目当前路径搜索部分不完善，战斗环节比较浪费时间，因此运行效率较低，暂时先开放旧都列车外围供大家刷取零号业绩(目前相对bug较少，运行相对比较稳定)，现在拿完零号业绩就跑路，后续会继续优化做到通关，来自动完成悬赏委托

本项目仅提供学习交流使用，

如果喜欢本项目，可右上角送作者一个`Star`

如有疑问，或者遇到bug，请到Issues提交问题，让遇到类似问题的朋友可以有地方找到相应的解决方案（[常见问题](#常见问题（及可能解决方法）)可能可以帮助解决部分疑惑）

QQ群`985508983`

## 前置条件
- 安装`Python3.10`以上版本
- 游戏窗口请设置为`1280X720`分辨率，窗口模式
- 脚本运行会占用键盘鼠标，在使用时不要操作键盘鼠标

## 安装教程
1. 下载本项目（或通过本页面上方绿色的Code-DownloadZIP直接下载解压文件并解压）
	```shell
	git clone https://github.com/sMythicalBird/ZenlessZoneZero-Auto.git
	cd ZenlessZoneZero-Auto
	```
	
2. 安装依赖（如果电脑没有Python运行环境，请先阅读[如何安装Python](#Python环境安装说明)）
   
   **！！！** GPU版本和CPU版本二选一
   
   * **GPU版本**
   
   > GPU版本使用前提是你的电脑上使用的是`Nvidia`显卡
   > 
   > CUDA版本请使用`11.8`，如果使用其他版本请参照[paddle安装文档](https://www.paddlepaddle.org.cn/install/quick)进行安装paddle
	> 
   >   
   如果你的电脑上没有安装`CUDA`、`CuDNN`，且不想安装`CUDA`、`CuDNN`，请使用以下命令进行安装`CUDA`、`CuDNN`依赖
   
   ```shell
   pip install -r requirements-cuda.txt
	```
	
	在确保你的电脑上已经安装了`CUDA`、`CuDNN`的情况下或已经安装上述依赖后，再使用以下命令进行安装依赖
	
	```shell
   pip install -r requirements.txt
   ```
	
   * **CPU版本**
	
	```shell
	pip install -r requirements-cpu.txt
	```

## 使用说明

> 请先打开游戏，进入零号空洞界面后，再运行脚本
> 

1. 以管理员权限打开shell后运行`main.py`文件（脚本必须以管理员权限运行）
	```shell
	python main.py
	```

## 视频演示

B站:https://www.bilibili.com/video/BV1hqb3eEEkh/?vd_source=6d82d7bb6e48d85193e2bb7c16eaa41c

## 小白版的自动安装工具
**注意**：
本工具使用certutil进行Python的下载，但certutil会被一些杀毒软件报毒，所以该工具有可能并未如预期工作。
所以，如果在运行本工具时出现"拒绝访问""找不到文件"等字样，您可以：
1.将本工具添加到杀毒软件的白名单。
2.删除本工具，按[这里](#Python运行环境安装说明（小白版，请严格按照步骤操作）)操作。
下面是杀毒软件的误报截图：![WindowsDefender.JPG](https://img.picui.cn/free/2024/07/16/669663656e70c.jpg) ![360.JPG](https://img.picui.cn/free/2024/07/16/669663657d500.jpg) ![火绒.JPG](https://img.picui.cn/free/2024/07/16/669663657441a.jpg)
将本项目克隆到本地后，打开本项目的文件夹，**右键单击**install.bat，选择“以管理员身份运行”，之后按照脚本提示操作。
请注意，在使用前需要将readme**完整**阅读一遍，特别是**安装依赖中的版本选择**与**常见问题**。


## Python运行环境安装说明（小白版，请严格按照步骤操作）
1. 首先下载[Windows installer (64-bit)](https://mirrors.huaweicloud.com/python/3.10.2/python-3.10.2-amd64.exe)，或前往[Python Releases for Windows | Python.org](https://www.python.org/downloads/windows/)下载最新版。
2. 运行安装包并成功安装后，后续操作都将在Windows Powershell中进行。在windows搜索栏（按键盘上的Win键呼出）搜索Windows Powershell，并点击“以管理员身份运行”。
3. 打开解压后的ZenlessZoneZero-Auto文件夹，选择任意文件夹，点击右键-属性，查看并复制位置信息（一般格式为“C:\\Users\\...\\ZenlessZoneZero-Auto”，...是省略的路径）。在powershell中运行（粘贴并点击回车）
``` shell
	cd C:\\Users\\...\\ZenlessZoneZero-Auto
```
4. 继续[安装教程](#安装教程)第二步，所有的命令都继续在这个Powershell的界面中运行，如果重新打开需要重复一遍步骤3的cd指令。


## 常见问题（及可能解决方法）
1. 任何提示“无法将...项识别为...”的提示，如果是git则可以通过直接下载本项目压缩包的形式绕过指令行直接下载，或[下载并安装git](https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe)。
2. 不知道指令在哪里输入的，或提示”No such file or directory“的，请查看[这里的第二步和第三步](#Python运行环境安装说明（小白版，请严格按照步骤操作）)。
3. 任何含有“version”这个关键词的错误信息，尝试运行
* **GPU版本**
   ```shell
	   pip install --upgrade -r requirements-cuda.txt
	   pip install --upgrade -r requirements.txt
   ```
* **CPU版本**
   ```shell
	   pip install -r requirements-cpu.txt
   ```
4.含有“动态链接库(DLL)初始化例程失败。”的错误信息，请尝试下载并安装[vc运行库](https://aka.ms/vs/17/release/vc_redist.x64.exe)
  如果不起作用，可以尝试运行:
  * **GPU版本**
    ```shell
            pip uninstall onnxruntime-gpu
	    pip install onnxruntime-gpu
    ```
  * **CPU版本**
  * ```shell
            pip uninstall onnxruntime
	    pip install onnxruntime
    ```

## 免责声明

本软件是一个外部工具旨在自动化绝区零的游戏玩法。并遵守相关法律法规。该软件包旨在减少用户游戏负担,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is an external tool designed to automate Jeopardy Zero's gameplay. and comply with relevant laws and regulations. This package is designed to provide simplicity and user interaction with the game through features, and it is not intended to upset the balance of the game in any way or provide any unfair advantage. This package does not modify any game files or game code in any way.

本软件开源、免费，仅供学习交流使用，禁止用于商业用途。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。
