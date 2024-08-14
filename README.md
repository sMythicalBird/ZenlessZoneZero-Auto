#  绝区零  零号空洞自动化框架2.2

> Tips:开发者最近在忙秋招，后续更新速度会放缓，大家见谅
> 
> 当前项目依旧处于开发阶段，很多地方还不完善，欢迎大家提出PR，一起完善这个项目。
>
> 本项目仅提供学习交流使用，如果觉得本项目做的不错，可右上角送作者一个`Star`

**！！！本项目开源免费，如果您遇到任何收费情况都属于被他人欺骗**

## 目录：

1. [项目简介](#项目简介)
2. [使用说明](#使用说明-前置条件)
3. [安装教程](#安装教程)
4. [安装教程-小白一键](#安装教程-小白一键)
5. [运行报错解决办法](#运行报错解决办法)
6. [快捷键说明](#快捷键说明)
7. [事件BUG说明](#事件BUG说明)
8. [后台运行](#后台运行)
9. [免责声明](#免责声明)




## 项目简介

绝区零 零号空洞自动化框架是一个基于`Python3.10`的自动化框架

本项目基于图像分类、模板匹配、OCR识别进行地图全局自动寻路和事件处理，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。

本项目的当前目标是可以让玩家从每周长时间的零号空洞材料刷取中解放出来，只需要在电脑上挂着就可以自动完成。本项目后续也会继续考虑增加其他自动化操作，帮助玩家做到日常托管。

**2.2.1优化内容**
   1. 重构了战斗逻辑，现在不会出现结束战斗后还在战斗中的情况
   2. 优化了事件处理，去掉了很多事件识别的延迟，事件处理更加稳定(开发者现在打核心比之前能快3-6分钟)

TODO:
   1. 1.1核心地区出现新地图，但是背景和之前有所不同，模型出现误判，后续有时间会重新训练数据集
   2. 项目相关文档正在整理，后续会部署到网站
   3. GUI界面已在开发中。
   4. 战斗逻辑设计已在开发中

如有疑问，或者遇到bug，请到Issues提交问题，让遇到类似问题的朋友可以有地方找到相应的解决方案（[常见问题](#常见问题（及可能解决方法）)可能可以帮助解决部分疑惑）

QQ群`985508983`

## 使用说明-前置条件

> 请先打开游戏，进入零号空洞界面后，再运行脚本

#### 1、脚本说明

本脚本主要适用于零号空洞每周五次委托奖励和零号业绩的刷取，每周五次通关后可以将脚本改成只刷零号业绩，拿到零号业绩就可以跑路。练度够的话推荐刷旧都列车前线，目前测试下来最快。

目前脚本适配性最好的地图是旧都列车，自动刷取建议选择旧都列车，低难本基本测试没问题，刷取每周五次委托奖励和零号业绩基本够用了。高难度副本目前支持内部和腹地，核心难度开发者练度不够目前打不过，数据集不全，模型识别可能会有问题，等后面开发者等级高了会继续进行测试。


#### 2、游戏内设置说明(下面几项严格按照要求来)
   > 如果脚本运行出现问题，请严格按照[推荐游戏设置](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/%E6%8E%A8%E8%8D%90%E6%B8%B8%E6%88%8F%E8%AE%BE%E7%BD%AE)设置游戏画面！
   >

   1. 设置->输入->棋盘镜头移动速度->1
   2. 设置->画面->显示模式->1280*720窗口
   3. 设置->键鼠设置->角色切换下一位->Space(战斗场景下的切人按键必须是Space)
   4. 脚本运行会占用键盘鼠标，在使用时不要操作键盘鼠标
   5. 脚本运行前游戏界面置于零号空洞副本选择界面
   6. 帧率设置为60帧，刷`拿命验收`的时候必须是60帧，否则会出现问题
   7. 显示屏防蓝光关闭，HDR也要关闭，否则影响截图做模板匹配
   8. 显示屏缩放比例设置为100%(4k屏自己测试一下不同缩放情况，一般150/250缩放比较合适)
   9. 目前脚本只支持游戏语言设置为简中，暂未对其他语言进行适配

#### 3、配置文件说明

1. 将项目文件夹下的`config.example.yaml`复制一份重命名为`config.yaml`文件

   参照`config.example.yaml`文件中的注释说明进行配置`config.yaml`文件的参数

   ```yaml
   #ZoneMap = {
   #    1: {
   #        "name": "旧都列车",
   #        "level": {1: "外围", 2: "前线", 3: "内部", 4: "腹地", 5: "核心"},
   #    },
   #    2: {
   #        "name": "施工废墟",
   #        "level": {1: "前线", 2: "内部", 3: "腹地", 4: "核心"},
   #    },
   #}
   
   # 模型训练集大部分来自旧都列车，脚本刷图目前旧都列车最稳定，其他图bug会比较多，刷零号业绩旧都列车前线最快，练度够可以直接刷前线
   targetMap:
       level: 1                # 默认等级 1: 外围
       zone: 1                 # 默认区域 1: 旧都列车
   modeSelect: 1               # 模式选择 1: 全通关  2: 刷零号业绩  3：零号银行  4：零号银行零号业绩一起
   maxFightTime: 300           # 最大战斗时间，单场战斗时间默认为300s，超过300s会重开(部分战斗场景需要跑图，目前还没进行相关处理，遇到这种情况会退掉重开)
   maxMapTime: 1500            # 在地图内最大时间默认为1500s，超过最大时间未通关地图会重开
   hasBoom: True               # 是否解锁炸弹
   useGpu: True                # 是否使用GPU，默认True, 使用GPU会加速模型训练,如果改为False，会强制使用CPU进行OCR识别
   selBuff: ["冻结", "暴击", "决斗", "闪避"]       # 鸣辉选择
   characters: ["艾莲", "莱卡恩", "苍角"]       # 自己带了哪些角色这里就填哪些，当然填了不一定有相应的战斗逻辑，后面版本再加
   ```

2. 将项目文件夹下`fight/tactics_defaults`下的所有文件复制到`fight/tactics`文件夹下。

   该项目下为战斗逻辑的默认伪代码设计，玩家可以根据自己的需求自行设计伪代码，后续会整理伪代码设计规则供玩家进行DIY
   
   `默认.yaml`为默认战斗逻辑，此外，玩家可自定义人物战斗逻辑，目前仅支持艾莲、莱卡恩、苍角。
   
   `红光.yaml`和`黄光.yaml`为红光和黄光判定后的动作逻辑，玩家也可自行编辑。
   
   此外，玩家甚至可以自定义人物技能施放逻辑，参考`艾莲技能.yaml`。普通模块每执行2次后，便会执行一次技能模块。

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
   
   详细安装教程:[Conda环境配置说明](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Conda环境配置说明)

   安装视频演示:[Conda环境配置演示](https://www.bilibili.com/video/BV1FS421d7rK)

3. 环境配置好后，输入

    ```shell
    python main.py
    ```

## 安装教程-小白一键

压缩包链接：[release链接](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/releases) | [夸克链接](https://pan.quark.cn/s/b33eaf2ffcfc)

1. 通过上述链接选择一个直接下载文件并解压
2. 在项目目录下以管理员权限运行`start.exe`
3. 选择3运行脚本

## 运行报错解决办法

1、出现`ImportError: DLl load failed while importing onnxruntime_pybindl1_state:动态链接库(DLL)初始化例程失败`，

如果之前安装过CUDA

```
pip uninstall onnxruntime-gpu
pip install onnxruntime-gpu==1.17
```

如果没安装过CUDA，或者更换onnxruntime-gpu版本无效，则更新[Microsoft Visual C++ 可再发行程序包]( https://aka.ms/vs/17/release/vc_redist.x64.exe)

## 快捷键说明

  ```shell
  F10  恢复运行
  F11  暂停运行
  F12  结束运行
  ```
## 事件BUG说明

遇到脚本无法处理的事件可以截图上传至[2.2测试bug汇总 ](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/issues/130)，截图使用链接提供的截图工具，截取图片后发在问题下的评论区，开发者看到会进行处理

## 后台运行

**！！！提醒：远程桌面部署比较麻烦，仅适用于部分有计算机基础和动手能力的同学使用，小白不推荐使用**

后台运行的功能实现是通过新建另外的用户，然后新用户远程桌面连接到本地，在远程桌面运行脚本。

非Server版本的Windows系统默认是不支持多用户同时远程桌面的，所以需要进行一些设置，具体设置方法请参考

[Windows多用户同时远程本地桌面](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Windows%E5%A4%9A%E7%94%A8%E6%88%B7%E5%90%8C%E6%97%B6%E8%BF%9C%E7%A8%8B%E6%9C%AC%E5%9C%B0%E6%A1%8C%E9%9D%A2)

## 免责声明

本软件是一个外部工具旨在自动化绝区零的游戏玩法。并遵守相关法律法规。该软件包旨在减少用户游戏负担,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is an external tool designed to automate ZenlessZoneZero's gameplay. and comply with relevant laws and regulations. This package is designed to provide simplicity and user interaction with the game through features, and it is not intended to upset the balance of the game in any way or provide any unfair advantage. This package does not modify any game files or game code in any way.

本软件开源、免费，仅供学习交流使用，禁止用于商业用途。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。
