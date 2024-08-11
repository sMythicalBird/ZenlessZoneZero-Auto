---
title: Quick Start
icon: gears
order: 4
category:
  - Use guide
tag:
  - Quick Start

editLink: false
prev: false
next: false
comment: false
---
## 1 Download Code

Please download source code from [ZenlessZoneZero-Auto-Release](https://github.com/sMythicalBird/ZenlessZoneZero-Auto/releases/tag/v2.2)

::: tip Tips
The `CPU version of the separate packaging` (`Zenlesszonezero-Auto.zip`) comes with the environment

If you want to use the `GPU version`, select `Source Code (ZIP)`

`Source code (tar.gz)` is a commonly used format for `linux`. At present, Zero Zero does not support the `Linux` system, we also do not support
:::

![Release](/image/release.png)

To decompress the code to any path, it is recommended to be **full English** Otherwise, unexpected errors may occur

![解压代码](/image/zip.png)

## 2 Installation Dependence

Run `start.exe`, you will see the following interface

::: warning Warning
The script must run as an administrator! Otherwise, the authority is not enough!
:::

![运行脚本](/image/runexe.png)

::: details Details
**1. Installation dependencies:** Use in the first run, the deployment environment

**2. Install the specified version dependencies:** The default version may not be applicable for you, you can choose to install it yourself. Xiaobai users, please don't move!

**3. Running script:** Started script, you must use it after installation and dependencies.

**4. Exit:** Exit the script
:::

Now we use it for the first time, choose `1. Installation dependencies`, we will see the following interface

![安装依赖](/image/depend.png)

If you do n’t know what to use, choose `0. Smart choice`, `CPU Version` will be very dependent on, about `5 GB`,` CPU Version `relatively smaller

::: details Details
**0. Intelligent selection:** Automatically judge the use of `CPU version` or `GPU version`

**1. Install CPU version:** Deployment `CPU` Environment and use the` CPU` Run script

**2. Install the GPU version:** Deploy the `GPU` environment and use the` GPU` to run the script. See [Settings](configure.md)

**3. Exit:** Exit the script
:::

Waiting for the installation, the program may be "not moving" in the middle, which is normal. The fast and slow download depends on your network speed

::: warning Warning
Please close your `Watt Tookit`! Some acceleration tools will cause `ssh` to fail, which will cause download failure

If you find an error related to `ssh`, please turn off the acceleration software
:::

If you don't have an accident, you can enjoy the convenience of the script

## 3 Tutorial

1. Do not move the mouse during operation

::: tip shortcut key
Need to press on the terminal, not in the game

**F10：** Restore

**F11：** Suspend operation

**F12：** Run
:::

2. Please run as an administrator

3. Configuration file description

Copy a copy of the `Config.example.yaml` under the project folder

Refer to the parameters of the annotation instructions of `Config.example.yaml` to configure the parameters of the configuration `config.yaml` file

```python
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

# Most of the model training sets come from the old capital trains. The script brushing is currently the most stable train. There will be more BUG in other pictures.
targetMap:
    level: 1                # Default level 1: 外围
    zone: 1                 # Default area 1: 旧都列车
modeSelect: 1               # Pattern selection 1: Quan Customs Clearance 2: Brush Zero performance 3: Zero Bank 4: Zero Bank No. 0 performance together
maxFightTime: 300           # The maximum battle time, the single battle time is default to 300s, and more than 300s will be reopened (some battle scenarios need to run the map, and the relevant process has not yet been processed.
maxMapTime: 1500            # The maximum time in the map defaults to 1500s, and the maximum time will be reopening without customs clearance.
hasBoom: True               # Whether to unlock the bomb
useGpu: True                # Whether to use GPU, default TRUE, using GPU will accelerate model training. If it is changed to FALSE, the CPU will be used for OCR recognition
selBuff: ["冻结", "暴击", "决斗", "闪避"]       # Minghui Choose
characters: ["艾莲", "莱卡恩", "苍角"]       # What roles you brought here, you can fill it out here. Of course, you may not have the corresponding fighting logic, and the next version is added
```

Copy all the files under the project folder `FIGHT/TACTICS_Defaults` to the` Fight/Tactics` folder

::: tip Tips
The project is designed for the default pseudo code of combat logic. Players can design the pseudo code according to their needs, and subsequently organize pseudo -code design rules for players to perform `diy`

**默认.yaml：** The default combat logic, in addition, players can customize the character's battle logic. At present, only Ailian, Laician, Cangjiao, Zhu Yu, Nicole

**红光&黄光.yaml：** For the action logic after the decision of Hongguang and Huang Guang, players can also edit themselves

In addition, players can even customize the logic of character skills, refer to **艾莲技能.yaml**. Once the ordinary module is executed twice, the skill module will be executed.
:::