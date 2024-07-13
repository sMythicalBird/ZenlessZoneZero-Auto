#  绝区零 自动化框架 零号空洞

>> 当前项目处于开发阶段，正在开发零号空洞的自动化操作，可能会有很多问题，欢迎大家提出PR，一起完善这个项目。


## 项目简介
绝区零 零号空洞自动化框架是一个基于`Python3.10`的自动化框架

本项目基于图像识别，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。本项目的当前目标是可以让玩家从每周长时间的零号空洞材料刷取中解放出来，只需要在电脑上挂着就可以自动完成。本项目后续也会继续考虑增加其他自动化操作，帮助玩家做到日常托管。

本项目当前路径搜索部分不完善，战斗环节比较浪费时间，因此运行效率较低，暂时先开放旧都列车外围供大家刷取零号业绩(目前相对bug较少，运行相对比较稳定)，现在拿完零号业绩就跑路，后续会继续优化做到通关，来自动完成悬赏委托

本项目仅提供学习交流使用，

如果喜欢本项目，可右上角送作者一个`Star`

如有疑问，可以提ISSUE或进QQ群`985508983`咨询。

## 前置条件
- 安装`Python3.10`以上版本
- 游戏窗口请设置为`1280X720`分辨率，窗口模式
- 脚本运行会占用键盘鼠标，在使用时不要操作键盘鼠标

## 安装教程
1. 下载本项目
	```shell
	git clone https://github.com/sMythicalBird/ZenlessZoneZero-Auto.git
	cd ZenlessZoneZero-Auto
	```
2. 安装依赖
   * GPU版本
   
   > GPU版本使用前提是你的电脑上使用的是`Nvidia`显卡
   > 
   
   如果你的电脑上没有安装`CUDA`、`CuDNN`，且不想安装`CUDA`、`CuDNN`，请使用以下命令进行安装`CUDA`、`CuDNN`依赖
	
   ```shell
   pip install -r requirements-cuda.txt
   ```
   
   在确保你的电脑上已经安装了`CUDA`、`CuDNN`的情况下或已经安装上述依赖后，再使用以下命令进行安装依赖

	```shell
	pip install -r requirements.txt
	```

   * CPU版本
   
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



## 免责声明

本软件是一个外部工具旨在自动化绝区零的游戏玩法。并遵守相关法律法规。该软件包旨在减少用户游戏负担,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is an external tool designed to automate Jeopardy Zero's gameplay. and comply with relevant laws and regulations. This package is designed to provide simplicity and user interaction with the game through features, and it is not intended to upset the balance of the game in any way or provide any unfair advantage. This package does not modify any game files or game code in any way.

本软件开源、免费，仅供学习交流使用，禁止用于商业用途。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。