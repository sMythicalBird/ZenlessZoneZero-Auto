#  绝区零  零号空洞自动化框架1.0

> 当前项目处于开发阶段，正在开发零号空洞的自动化操作，可能会有很多问题，欢迎大家提出PR，一起完善这个项目。本项目仅提供学习交流使用，如果喜欢本项目，可右上角送作者一个`Star`



## 目录：

1. [项目简介](#项目简介)
2. [使用说明](#使用说明(前置条件))
3. [安装教程](#安装教程)
4. [安装教程-懒人版](#安装教程(纯小白，或依赖懒得自己动手配置))
5. [快捷键说明](#快捷键说明)
6. [事件BUG说明](#事件BUG说明)
7. [后台运行](#后台运行)
10. [免责声明](#免责声明)




## 项目简介

绝区零 零号空洞自动化框架是一个基于`Python3.10`的自动化框架

本项目基于图像分类、模板匹配、OCR识别进行地图全局自动寻路和事件处理，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。

本项目的当前目标是可以让玩家从每周长时间的零号空洞材料刷取中解放出来，只需要在电脑上挂着就可以自动完成。本项目后续也会继续考虑增加其他自动化操作，帮助玩家做到日常托管。

如有疑问，或者遇到bug，请到Issues提交问题，让遇到类似问题的朋友可以有地方找到相应的解决方案（[常见问题](#常见问题（及可能解决方法）)可能可以帮助解决部分疑惑）

QQ群`985508983`

## 使用说明(前置条件)

> 请先打开游戏，进入零号空洞界面后，再运行脚本

#### 1、脚本说明

本脚本主要适用于零号空洞每周五次委托奖励和零号业绩的刷取，每周五次通关后可以将脚本改成只刷零号业绩，拿到零号业绩就可以跑路。练度够的话推荐刷旧都列车前线，目前测试下来最快。

目前脚本适配性最好的地图是旧都列车，自动刷取建议选择旧都列车，低难本基本测试没问题，刷取每周五次委托奖励和零号业绩基本够用了。高难度副本不建议使用，开发者练度不够打不过，数据集不全，模型识别可能会有问题，等后面开发者等级高了会继续进行测试。

#### 2、游戏内设置说明(下面几项严格按照要求来)

1. 设置->输入->棋盘镜头移动速度->1
2. 设置->画面->显示模式->1280*720窗口
3. 设置->键鼠设置->角色切换下一位->Space
4. 脚本运行会占用键盘鼠标，在使用时不要操作键盘鼠标
5. 脚本运行前游戏界面置于零号空洞副本选择界面

#### 3、配置文件说明

1. 将项目文件夹下的`config.example.yaml`复制一份重命名为`config.yaml`文件

2. 参照`config.example.yaml`文件中的注释说明进行配置`config.yaml`文件的参数

   ```yaml
   targetMap:
   	zone: 1
   	level: 1 
   wholeCourse: false
   maxFightTime: 150
   maxMapTime: 900
   ```

3. 以管理员权限打开shell后运行`main.py`文件（脚本必须以管理员权限运行）

  ```shell
python main.py
  ```

## 安装教程

本项目提供通过conda创建安装环境的使用说明(有能力的可以通过其他方式部署项目，本项目不再做详细说明)

1. 下载本项目
	```shell
	git clone https://github.com/sMythicalBird/ZenlessZoneZero-Auto.git
	cd ZenlessZoneZero-Auto
	```
	
2. conda安装相关依赖
   
   **！！！** GPU版本和CPU版本二选一，GPU版本使用前提是你的电脑上使用的是`Nvidia`显卡
   
   详细安装链接:[Conda环境配置说明](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Conda环境配置说明)

3. 环境配置好后，输入

    ```shell
    python main.py
    ```

## 安装教程(纯小白，或依赖懒得自己动手配置)

1. 通过本页面上方绿色的Code-DownloadZIP直接下载解压文件并解压
2. 在云盘下载对应的环境压缩包(已打包好所有依赖)
	>  GPU版和CPU版二选一，选择GPU的前提是你电脑上使用的是`Nvidia`显卡
   
	GPU环境链接:
	CPU环境链接:
3. 将下载好的环境解压到项目目录下(ZenlessZoneZero-Auto)

4. 在项目目录下运行

## 快捷键说明

  ```shell
  F10  恢复运行
  F11  暂停运行
  F12  结束运行
  ```
## 事件BUG说明

遇到脚本无法处理的事件可以截图上传至[1.0正式版本异常事件汇总 ](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/issues/38)，截图使用链接提供的截图工具，截取图片后发在问题下的评论区，开发者看到会进行处理

## 后台运行

**！！！提醒：远程桌面部署比较麻烦，仅适用于部分有计算机基础和动手能力的同学使用，小白不推荐使用**

后台运行的功能实现是通过新建另外的用户，然后新用户远程桌面连接到本地，在远程桌面运行脚本。

非Server版本的Windows系统默认是不支持多用户同时远程桌面的，所以需要进行一些设置，具体设置方法请参考

[Windows多用户同时远程本地桌面](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Windows%E5%A4%9A%E7%94%A8%E6%88%B7%E5%90%8C%E6%97%B6%E8%BF%9C%E7%A8%8B%E6%9C%AC%E5%9C%B0%E6%A1%8C%E9%9D%A2)

## 免责声明

本软件是一个外部工具旨在自动化绝区零的游戏玩法。并遵守相关法律法规。该软件包旨在减少用户游戏负担,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is an external tool designed to automate Jeopardy Zero's gameplay. and comply with relevant laws and regulations. This package is designed to provide simplicity and user interaction with the game through features, and it is not intended to upset the balance of the game in any way or provide any unfair advantage. This package does not modify any game files or game code in any way.

本软件开源、免费，仅供学习交流使用，禁止用于商业用途。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。
