#  绝区零  零号空洞自动化框架2.3

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

v2.3演示：https://www.bilibili.com/video/BV1ZSpreFEKJ/

**2.3.1版本追加更新：**

 1. 更换图片分类模型，现在可以正确识别1.1版本新加的黑色背景格
 2. 启动器新加了拿命验收选项，现在启动脚本会进行功能选择 

**2.3优化内容**

 1. 重构了战斗逻辑，战斗部分通过子线程调用进行，现在不会出现结束战斗后还在战斗中的情况
 2. 优化了事件处理，去掉了很多事件识别的延迟，事件处理更加稳定(开发者现在打核心比之前能快3-6分钟)，部分奖励事件优先选择回血
 3. 鉴于1.1版本增加了第三层的业绩数量。零号空洞模式选择4不再支持银行业绩同时采集，改为全通模式(含业绩)版，现在模式2和4均会收取所有业绩(拿不到s评价会退出)。
 4. 增加了部分角色(青衣，11号)的战斗逻辑
 5. 修复部分bug：领完业绩后不再会呆在原地发呆，战斗结束后不会继续战斗，部分运行卡顿问题进行优化



**TODO(后续版本会陆续优化):**

1. 1.1核心地区出现新地图，但是背景和之前有所不同，模型出现误判，后续有时间会重新训练数据集
2. 项目相关文档正在整理，后续会部署到网站
3. GUI界面已在开发中。
4. 战斗逻辑设计已在开发中
   



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

#### 2、配置文件说明

1. 将项目文件夹下的`config.example.yaml`复制一份重命名为`config.yaml`文件

   参照`config.example.yaml`文件中的注释说明进行`config.yaml`文件的参数配置

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
       level: 3                # 默认等级 1: 外围
       zone: 1                 # 默认区域 1: 旧都列车
   modeSelect: 4               # 模式选择 1: 全通关  2: 刷零号业绩  3：零号银行  4：全通关(拾取业绩,级别不够会退出)
   maxFightTime: 300           # 最大战斗时间，单场战斗时间默认为300s，超过300s会重开(部分战斗场景需要跑图，目前还没进行相关处理，遇到这种情况会退掉重开)
   maxMapTime: 1500            # 在地图内最大时间默认为1500s，超过最大时间未通关地图会重开
   hasBoom: True               # 是否解锁炸弹
   useGpu: True                # 是否使用GPU，默认True, 使用GPU会加速模型训练,如果改为False，会强制使用CPU进行OCR识别
   selBuff: ["冻结", "暴击", "决斗", "闪避"]       # 鸣辉选择
   characters: ["艾莲", "莱卡恩", "苍角"]       # 自己带了哪些角色这里就填哪些，当然填了不一定有相应的战斗逻辑，后面版本再加
   maxFightCount: 100          # 最大空洞完成次数，超过最大战斗次数会退出
   teamMates: 2                # 战斗中可寻找的队友数量，最大值为2，最小值为0
   ```

   

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
