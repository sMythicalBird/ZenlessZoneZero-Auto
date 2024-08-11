---
title: Environment
icon: terminal
order: 4
category:
  - Use guide
tag:
  - Environment

editLink: false
prev: false
next: false
comment: false
---

## 1 Hadware Configure

::: details Your computer system version must not be a version of Windows 7 and below
Because `python` has given up support for `Windows 7` in `3.9`, and our script is based on `3.10`, so we cannot start it depend on the `Windows 7`

We recommend using `Python 3.10`, and you can also try to change the environment to `Python 3.8`. We are **not responsible for the problem caused by the replacement version**
:::

::: details If you use the `GPU version`, you must have a NVIDIA graphics card

`GPU Version` based on `CUDA`, will not be available if there is no `NVIDIA graphics card`
You need to install `requirements-dml.txt`. You may need to run the following code or use the `Start.exe` directly and select `Installation dependencies, select the GPU version `

```bash
.\py310\python -m pip -r install .\\requirements-dml.txt
```
:::

## 2 System Setting

::: details The system cannot open the HDR mode and night mode
`HDR mode` and `Night mode` will make the screenshot of produce the difference between overexposure or color sets, which leads to the mix of the template

Please press `Windows + Q` input `Display Settings`

![搜索显示器](/image/MonitorSearch.png)

Close `HDR mode` and `Night mode`

![关闭HDR和夜间模式](/image/MonitorSetting.png)
:::

::: details The screen scaling of the system must be 100%
If your screen zoom is not `100%`, it will cause `OCR Recognition` to fail, which will affect the use

Please press `Windows + Q` input` Display Settings `

![搜索显示器](/image/MonitorSearch.png)

Substarant to `100%`
`
![DPI](/image/DPI.png)

:::

::: details The system cannot overclock, if you overclock the CPU / GPU, please turn off

Overclocking will affect key components `Onxruntime`, which causes image recognition errors. We don't know how to solve it at present

:::

## 3 Game Settings

::: details The game window size is set to 1280x720 window, and the number of frames is limited to 60 frames
In order to avoid accidents, we use the size of the size in the test environment. The main reason is that we use template matching. If it is not consistent, it will cause failure

`拿命验收` The task must be `60 frames`, otherwise there will be problems

![游戏设置](/image/GameSettings.png)
:::

::: details Font recommendation is set to global fine
Zoneless Zone Zero The fonts are very unclear. Modification to fineness can effectively improve the accuracy of identification

![字体设置](/image/FontSettings.png)
:::

::: details The game language must be Chinese
The currently marked data sets are Chinese, and do not support other languages

![语言设置](/image/LanguageSettings.png)
:::

::: details Cut the keys must be Space
The yellow light bomb knife button set by the program is `Space`, you use other keys to cause the knife to be unable to play the knife

![按键设置](/image/ControlSettings.png)
:::

::: details The game interface should be placed on the zero empty hole in the program when running
The current program is only supported in the 零号空洞 , 
the others are not supported

![界面设置](/image/Page.png)
:::