#  绝区零  零号空洞自动化框架2.4.0

> Tips:开发者最近在忙秋招，后续更新速度会放缓，大家见谅


> 当前项目依旧处于开发阶段，很多地方还不完善，欢迎大家提出PR，一起完善这个项目。
>
> 本项目仅提供学习交流使用，如果觉得本项目做的不错，可右上角送作者一个`Star`

**！！！本项目开源免费，如果您遇到任何收费情况都属于被他人欺骗**

## 目录：

1. [项目简介](#项目简介)
2. [使用说明](#使用说明)
3. [使用教程-小白一键](#使用教程-小白一键)
4. [使用教程-进阶](#使用教程-进阶)
5. [运行报错解决办法](#运行报错解决办法)
6. [免责声明](#免责声明)




## 项目简介

绝区零 零号空洞自动化框架是一个基于`Python3.10`的自动化框架

本项目基于图像分类、模板匹配、OCR识别进行地图全局自动寻路和事件处理，不涉及任何游戏内部数据的修改，不会对游戏内部数据造成任何影响。

本项目的当前目标是可以让玩家从每周长时间的零号空洞材料刷取中解放出来，只需要在电脑上挂着就可以自动完成。本项目后续也会继续考虑增加其他自动化操作，帮助玩家做到日常托管。

本脚本主要适用于零号空洞每周委托奖励和零号业绩的刷取，每周通关到达次数要求后可以将脚本改成只刷零号业绩，拿到零号业绩就可以跑路。业绩模式推荐列车腹地，一层150，打得也快。

目前脚本适配性最好的地图是旧都列车，自动刷取建议选择旧都列车。

##### 2.4更新

1. 新增gui界面，新增兑换码批量兑换功能、战斗diy设计功能
2. 重新调整参数和模块结构
3. 更新零号空洞图片分类模型



**TODO(后续版本会陆续优化):**



往期优化内容详情见[更新日志 ](https://fairy.autoscript.site/zh/community/updatelog.html)

如有疑问，或者遇到bug，请到[Issues](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/issues)提交问题，让遇到类似问题的朋友可以有地方找到相应的解决方案

交流QQ群：`985508983`

项目详细使用说明可以查看项目主页：https://fairy.autoscript.site/zh/  

特此感谢[IsSmallPigPig](https://github.com/IsSmallPigPig)为本项目编写了详细的文档说明



## 使用说明

> 请先打开游戏，进入零号空洞界面后，再运行脚本


#### 1、游戏内设置说明(下面几项严格按照要求来)
   > 如果脚本运行出现问题，请严格按照[推荐游戏设置](https://fairy.autoscript.site/zh/demo/required.html)设置游戏画面！
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
      10. 游戏字体设置为细体



## 使用教程-小白一键

压缩包链接：[release链接](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/releases) | [夸克链接](https://pan.quark.cn/s/b33eaf2ffcfc)

1. 通过上述链接选择一个直接下载最新版文件并解压
2. 在项目目录下以管理员权限运行`start.exe`
3. 按照使用说明配置好，选择3运行脚本



## 使用教程-进阶

> 本部分是cuda和远程桌面的配置，小白可以跳过，直接使用上面的一键版本

本项目提供通过conda创建安装环境的使用说明(有能力的可以通过其他方式部署项目，本项目不再做详细说明)

#### conda安装相关依赖

**！！！** GPU版本和CPU版本二选一，GPU版本使用前提是你的电脑上使用的是`Nvidia`显卡

详细安装教程：[Conda环境配置说明(wiki)](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Conda环境配置说明)  [Conda环境配置说明(文档)](https://fairy.autoscript.site/zh/demo/configure.html)

安装视频演示：[Conda环境配置演示](https://www.bilibili.com/video/BV1FS421d7rK)

#### 后台运行(远程桌面配置)

详细安装教程：[Windows多用户同时远程本地桌面(wiki)](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/wiki/Windows%E5%A4%9A%E7%94%A8%E6%88%B7%E5%90%8C%E6%97%B6%E8%BF%9C%E7%A8%8B%E6%9C%AC%E5%9C%B0%E6%A1%8C%E9%9D%A2) | [Windows多用户同时远程本地桌面](https://fairy.autoscript.site/zh/demo/configure.html)



## 运行报错解决办法

1、出现`ImportError: DLl load failed while importing onnxruntime_pybindl1_state:动态链接库(DLL)初始化例程失败`，

如果之前安装过CUDA

```
pip uninstall onnxruntime-gpu
pip install onnxruntime-gpu==1.17
```

如果没安装过CUDA，或者更换onnxruntime-gpu版本无效，则更新[Microsoft Visual C++ 可再发行程序包]( https://aka.ms/vs/17/release/vc_redist.x64.exe)



## 免责声明

本软件是一个外部工具旨在自动化绝区零的游戏玩法。并遵守相关法律法规。该软件包旨在减少用户游戏负担,并且它不打算以任何方式破坏游戏平衡或提供任何不公平的优势。该软件包不会以任何方式修改任何游戏文件或游戏代码。

This software is an external tool designed to automate ZenlessZoneZero's gameplay. and comply with relevant laws and regulations. This package is designed to provide simplicity and user interaction with the game through features, and it is not intended to upset the balance of the game in any way or provide any unfair advantage. This package does not modify any game files or game code in any way.

本软件开源、免费，仅供学习交流使用，禁止用于商业用途。开发者团队拥有本项目的最终解释权。使用本软件产生的所有问题与本项目与开发者团队无关。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。
