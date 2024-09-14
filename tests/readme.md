<!--
 * @Descripttion: 
 * @Author: White
 * @Date: 2024-09-09 12:42:25
 * @LastEditTime: 2024-09-14 18:38:23
-->
# 描述
这是一个自动化测试的模块，旨在为项目发版前提供自动化测试并且生成报告。现有功能有测试页面跳转、零号空洞任务、设置页面。

# 环境
```python
# 安装模块
pip install pytest
pip install pyautogui
pip install pytest-html
```
```
设置系统缩放为100%
若测试外链接跳转，浏览器不能全屏（会影响测试）
```
```
zero.yaml和fight.yaml提前配置，测试时maxFightCount建议设置为1，modeSelect设置为4,  level设为1，zone设为1
```
# 运行命令
注意事项：启动前先将游戏窗口打开，执行启动命令后鼠标点击空白位置（防止Fairy Auto窗口不展示）

```powershell
# 环境：powershell
# 执行全部测试用例并且生成报告report.html
cd ZenlessZoneZero-Auto
$env:PYTHONPATH = "$env:PYTHONPATH;."
pytest --html=.\tests\report\report.html .\tests\test_gui.py  # 若要详细输出信息，加上-s参数
```

# 测试用例编写说明
```python
# 测试用例默认存放于test\testcase下
# 格式样例如下：
testcase:  # 默认开头
  - des: "测试页面跳转,首页->战斗设计"  # 测试用例描述
    steps:  # 操作步骤
    -
      - page_redirection  # 页面跳转函数
      - dst_page=dom.navagation.fightedit.0  # 函数传参
      - window=dom.window  # 函数传参
    assert_:   # 断言
    - get_cur_widge_name  # 断言函数
    - obj=dom.window  # 函数传参
    - dom.navagation.fightedit.0  # 要判断的值
# steps下可以有多个操作步骤。每个操作步骤第一个值默认写函数名，剩余值填函数调用需要的参数，以key=value的方式传参
# assert_下的断言函数只能有一个，默认第一个值写函数名，第二个值写函数参数（断言函数最多有1个传参，不传参可空着）
# dom开头的传参有特定要求，下边会进行说明
````
steps可填函数：

|功能|函数名|参数|参数说明|返回值|
| :--: | :--: | :--: |  :--: | :--: |
|页面跳转|page_redirection|dst_page,window|dst_page字符串类型，值为目标页面的objectName。window要填dom.window| None|
|控件点击|widget_click|widget|QWidget类型，值为控件对象|None|

assert_可填函数：

|功能|函数名|参数|参数说明|返回值|
| :--: | :--: | :--: |  :--: | :--: |
|获取当前widget的objectName|get_cur_widge_name|obj|可填有stackedWidget属性的任何对象|返回obj的objectName，为字符串类型|
|屏幕截图比较是否有特定字符出现|screenshot_and_compare|s|字符串类型，通常填要断言的值|如果识别出包含s返回列表，否则返回空列表|

dom说明：

|目标|获取到的方式|
| :--: | :--: |
|获取window|dom.window|
|获取主页面的objectName|dom.navagation.home.0|
|获取战斗设计页面的objectName|dom.navagation.fightedit.0|
|获取兑换码页面的objectName|dom.navagation.code.0|
|获取配置页面的objectName|dom.navagation.config.0|
|获取设置页面的objectName|dom.navagation.setting.0|
|获取主页面的github卡片对应的widget|dom.home.widgets.github.obj_|
|获取主页面的项目卡片对应的widget|dom.home.widgets.site.obj_|
|获取主页面的零号空洞任务卡片对应的widget|dom.home.widgets.zero_task.obj_|
|获取设置页面更新标签对应的widget|dom.setting.widgets.update.obj_|
|获取配置页面的obj|dom.setting.obj_|
|获取配置页面更新卡片标签的objectName|dom.setting.widgets.update.name|
