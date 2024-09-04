#  绝区零自动化框架2.4.0

> Tips:开发者最近在忙秋招，后续更新速度会放缓，大家见谅


> 当前项目依旧处于开发阶段，很多地方还不完善，欢迎大家提出PR，一起完善这个项目。
>
> 本项目仅提供学习交流使用，如果觉得本项目做的不错，可右上角送作者一个`Star`

**！！！本项目开源免费，如果您遇到任何收费情况都属于被他人欺骗**

## 目录：

1. [项目简介](#项目简介)
2. [使用教程](#使用教程)
3. [使用教程-进阶](#使用教程-进阶)
6. [免责声明](#免责声明)




## 项目简介

绝区零自动化项目是一个基于`Python3.10`的自动化项目

本项目基于图像分类、模板匹配、OCR识别进行地图全局自动寻路和事件处理，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。

战斗模块目前逻辑组不全，欢迎大家多多提交新的逻辑设计。

目前零号空洞适配性最好的地图是旧都列车，自动刷取建议选择旧都列车。

##### 2.4.0更新

1. 新增gui界面，新增兑换码批量兑换功能、战斗diy设计功能，更新功能
2. 重新调整参数和模块结构
3. 更新零号空洞图片分类模型

**TODO**

其他功能

往期优化内容详情见[更新日志 ](https://fairy.autoscript.site/zh/community/updatelog.html)

如有疑问，或者遇到bug，请到[Issues](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/issues)提交问题，让遇到类似问题的朋友可以有地方找到相应的解决方案

交流QQ群：`985508983`



## 使用教程

压缩包链接：[release链接](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/releases) | [夸克链接](https://pan.quark.cn/s/b33eaf2ffcfc)

1. 通过上述链接选择一个直接下载最新版文件并解压
2. 在项目目录下以管理员权限运行`start.exe`
3. 按照使用说明配置好，选择3运行脚本

部分功能视频演示见：https://space.bilibili.com/276027372

项目详细使用说明可以查看项目主页：https://fairy.autoscript.site/zh/  

特此感谢[IsSmallPigPig](https://github.com/IsSmallPigPig)为本项目编写了详细的文档说明



## 使用教程-进阶

> 本部分是cuda和远程桌面的配置，小白可以跳过，直接使用上面的一键版本

本项目提供通过conda创建安装环境的使用说明(有能力的可以通过其他方式部署项目，本项目不再做详细说明)

#### conda安装相关依赖

**！！！** GPU版本和CPU版本二选一，GPU版本使用前提是你的电脑上使用的是`Nvidia`显卡

详细安装教程：[Conda环境配置说明(wiki)](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Conda环境配置说明)  [Conda环境配置说明(文档)](https://fairy.autoscript.site/zh/demo/configure.html)

安装视频演示：[Conda环境配置演示](https://www.bilibili.com/video/BV1FS421d7rK)

#### 后台运行(远程桌面配置)

详细安装教程：[Windows多用户同时远程本地桌面(wiki)](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Windows%E5%A4%9A%E7%94%A8%E6%88%B7%E5%90%8C%E6%97%B6%E8%BF%9C%E7%A8%8B%E6%9C%AC%E5%9C%B0%E6%A1%8C%E9%9D%A2) | [Windows多用户同时远程本地桌面](https://fairy.autoscript.site/zh/demo/configure.html)





## 免责声明

本软件是一个外部工具旨在自动化绝区零的游戏玩法。并遵守相关法律法规。该软件包旨在减少用户游戏负担,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is an external tool designed to automate ZenlessZoneZero's gameplay. and comply with relevant laws and regulations. This package is designed to provide simplicity and user interaction with the game through features, and it is not intended to upset the balance of the game in any way or provide any unfair advantage. This package does not modify any game files or game code in any way.

本软件开源、免费，仅供学习交流使用，禁止用于商业用途。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。
