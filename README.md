#  绝区零 零号空洞自动化框架

>> 当前项目处于开发阶段，运行效率极低，可能会有很多问题，欢迎大家提出PR，一起完善这个项目。


## 项目简介
绝区零 零号空洞自动化框架是一个基于`Python3.10`的自动化框架

本项目基于图像识别，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。

仅提供学习交流使用，禁止用于商业用途。

## 前置条件
- 安装`Python3.10`以上版本
- 游戏窗口请设置为`1280X720`分辨率，窗口模式
- 脚本运行会占用键盘鼠标，在使用时不要操作键盘鼠标

## 安装教程
1. 下载本项目
	```shell
	git clone  ...
	cd ..
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

1. 运行`main.py`文件
	```shell
	python main.py
	```