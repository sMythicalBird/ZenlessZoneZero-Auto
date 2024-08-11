---
title: 配置环境
icon: terminal
order: 4
category:
  - 使用指南
tag:
  - 配置环境

editLink: false
prev: false
next: false
comment: false
---

## 1 硬件配置

::: details 您的电脑系统版本不得是 Windows 7 及以下的版本
因为 `Python` 在 `3.9` 就已经放弃了对 `Windows 7` 的支持，而我们的脚本是基于 `3.10` 的，所以我们无法在 `Windows 7` 下启动

::: warning 注意事项
我们推荐使用 `Python 3.10`，您也可以尝试自行更换环境到 `Python 3.8`。我们对更换版本造成的问题 **概不负责**
:::

::: details 如果您使用 GPU 版本，则必须有一张 NVIDIA 的显卡

`GPU 版本` 基于 `CUDA`，没有 `NVIDIA` 显卡的将无法使用

::: tip 解决方案
您需要安装 `requirements-dml.txt`。您可能需要运行以下代码或者直接使用 `start.exe` 并选择 `安装依赖`，选择 `安装 GPU 版本`

```bash
.\py310\python -m pip -r install .\\requirements-dml.txt
```
:::

## 2 系统设置

::: details 系统不能开启 HDR 模式 和 夜间模式
`HDR 模式` 和 `夜间模式`  会让 `截图` 与数据集产生过曝或偏色的差别，从而导致 `模板匹配` 失败

::: tip 解决方案
请按 `Windows + Q` 输入 `显示器设置`

![搜索显示器](/image/MonitorSearch.png)

关闭 `HDR 模式` 和 `夜间模式`

![关闭HDR和夜间模式](/image/MonitorSetting.png)
:::

::: details 系统的屏幕缩放必须是 100%
如果您的屏幕缩放不是 `100%`，则会导致 `OCR 识别` 失败，从而影响使用 

::: tip 解决方案
请按 `Windows + Q` 输入 `显示器设置`

![搜索显示器](/image/MonitorSearch.png)

将 `缩放` 改为 `100%`

![DPI](/image/DPI.png)

:::

::: details 系统不能超频，如果您超频了 CPU / GPU，请关闭

超频将会影响关键组件 `onnxruntime`，导致图像识别错误。我们目前并不清楚怎么解决

:::

## 3 游戏设置

::: details 游戏窗口大小设置为 1280x720 窗口，帧数限制为 60 帧
为了避免意外问题，我们统一使用测试环境下大小的窗口。主要原因是因为我们采用了模板匹配，如果不一致会导致失效

`拿命验收` 的任务必须是 60 帧，否则会出现问题
::: tip 解决方案
![游戏设置](/image/GameSettings.png)
:::

::: details 字体建议设置为全局细体
绝区零的字体很不清晰，修改为细体能有效改善识别精准度
::: tip 解决方案
![字体设置](/image/FontSettings.png)
:::

::: details 游戏语言必须是中文
当前标注的数据集都是中文，不支持其他语言
::: tip 解决方案
![语言设置](/image/LanguageSettings.png)
:::

::: details 切人按键必须是 Space
程序设定的黄光弹刀按键为 `Space`，您使用其他按键会导致无法弹刀
::: tip 解决方案
![按键设置](/image/ControlSettings.png)
:::

::: details 程序运行时游戏界面要置于零号空洞副本选择界面
目前程序仅支持在 零号空洞 中刷图，其他均不支持
::: tip 解决方案
![界面设置](/image/Page.png)
:::