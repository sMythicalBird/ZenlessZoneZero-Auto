'''
Descripttion: 测试Gui，目前可测功能为页面跳转、首页、设置页面
Author: White
Date: 2024-09-09 12:43:50
LastEditTime: 2024-09-14 17:56:20
'''
import sys
import pytest
from PySide6.QtWidgets import QApplication, QWidget, QLayout
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from gui.main_window import MainWindow
from schema.download import check_file_task
from paddleocr import PaddleOCR
from gui.home_interface import BannerWidget, TaskCardView
from gui.fight_edit_interface import DesignerGroup
from gui.components.designer_card import DesignerCard, CombiningWidget1, CombiningWidget2
from gui.components.task_card import TaskCard
import pyautogui
import os
import re
import yaml
import win32gui
import cv2
import win32con


HOME = "HomeInterface"
FIGHTEDIT = "FightEditInterface"
CODE = "CodeInterface"
CONFIG = "ConfigInterface"
SETTING = "SettingInterface"
current_directory = os.path.dirname(__file__)
TESTCASE_ROOT = current_directory + os.sep + "testcase"
UPDATE = "update_group"
README = "readme_group"


class Page:
    def __init__(self, name, obj_) -> None:
        self.widgets = {}
        self.name = name
        self.obj_ = obj_
        pass


class Widge:
    def __init__(self, name, obj_) -> None:
        self.name = name
        self.obj_ = obj_

    
class Dom:
    """解析Gui"""
    def __init__(self, window: MainWindow) -> None:
        self.window = window
        self.analise(window)
    
    def get_all_widgets(self, layout: QLayout):  
        """  
        递归函数，用于获取布局中的所有控件。          
        :param layout: QLayout的实例，要遍历的布局。  
        :return: 包含所有控件的列表。  
        """  
        widgets = []  
        for i in range(layout.count()):  
            item = layout.itemAt(i)  
            if isinstance(item.widget(), QWidget):  
                widgets.append(item.widget())  
            elif isinstance(item.layout(), QLayout):  
                widgets.extend(self.get_all_widgets(item.layout()))  
            if isinstance(item.widget(), BannerWidget):  
                widgets.extend(self.get_all_widgets(item.widget().vBoxLayout)) 
            elif isinstance(item.widget(), TaskCardView):   
                widgets.extend(self.get_all_widgets(item.widget().flowLayout)) 
            elif isinstance(item.widget(), DesignerGroup):  
                widgets.extend(self.get_all_widgets(item.widget().vBoxLayout))  
            elif isinstance(item.widget(), DesignerCard):
                widgets.extend(self.get_all_widgets(item.widget().hBoxLayout))     
            elif isinstance(item.widget(), CombiningWidget1):
                widgets.extend(self.get_all_widgets(item.widget().hBoxLayout))    
            elif isinstance(item.widget(), CombiningWidget2):
                widgets.extend(self.get_all_widgets(item.widget().hBoxLayout))                                                                          
        return widgets 
    
    def window_analyze(self, window):
        navigation_info = {}
        pages_info = {}
        # 获取页面
        for i in range(window.stackedWidget.count()):
            page = window.stackedWidget.widget(i)
            pages_info[page.objectName()] = {"page": page}
        # 获取导航
        for n, b in window.navigationInterface.items.items():
            navigation_info[n] = b
        home = window.stackedWidget.currentWidget() 
        pages_info[HOME] = {"page": home}
        # 获取页面上的所有控件
        for n, info in pages_info.items():
            widgets = self.get_all_widgets(info["page"].vBoxLayout)
            for widget in widgets:
                widget_n = type(widget).__name__
                info[widget_n] = info.get(widget_n, []) + [widget]
        return navigation_info, pages_info
    
    def analise(self, window):
        n, p = self.window_analyze(window)
        # 导航
        self.navagation = {
            "home": (HOME, n[HOME]),
            "fightedit": (FIGHTEDIT, n[FIGHTEDIT]),
            "code": (CODE, n[CODE]),
            "config": (CONFIG, n[CONFIG]),
            "setting": (SETTING, n[SETTING])
        }
        # 页面
        self.home = Page("home", p[HOME]["page"])
        self.fightedit = Page("fightedit", p[FIGHTEDIT]["page"])
        self.code = Page("code", p[CODE]["page"])
        self.config = Page("config", p[CONFIG]["page"])
        self.setting = Page("setting", p[SETTING]["page"])
        # 控件
        self.home.widgets = {
            "github": Widge("github", p[HOME]["LinkCardView"][0]),
            "site": Widge("site", p[HOME]["LinkCardView"][1]),
            "zero_task": Widge("zero_task", p[HOME]["TaskCard"][0]) 
        }
        self.fightedit.widgets = {}
        self.code.widgets = {}
        self.config.widgets = {}
        pivot = self.setting.obj_.pivot
        navigation_info = {}
        for n, b in pivot.items.items():
            navigation_info[n] = b
        self.setting.widgets = {
            "update": Widge(UPDATE, navigation_info[UPDATE]),
            "readme": Widge(README, navigation_info[README])
        }


def load_testcase():
    data_list = []
    for f_n in os.listdir(TESTCASE_ROOT):
        f_p = os.path.join(TESTCASE_ROOT, f_n)
        with open(f_p, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            data_list += data["testcase"]
    return data_list
        

def load_one_testcase(f_n):
    f_p = os.path.join(TESTCASE_ROOT, f_n)
    with open(f_p, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data["testcase"]


@pytest.fixture(scope="module")
def app():
    _app = QApplication(sys.argv)
    yield _app
    _app.quit()    
    pyautogui.press('f12')
    

@pytest.fixture
def window(app):
    _window = MainWindow()
    # screen = _window.screen()
    # w, h = screen.size().width(), screen.size().height()
    # pyautogui.click(0, h-10)
    # pyautogui.click(0, h-10)
    _window.show()
    QTest.qWaitForWindowExposed(_window)
    _dom = Dom(_window)
    hwnd = win32gui.FindWindow(None, _window.windowTitle())
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    yield _window, _dom
    _window.close()


@pytest.fixture(scope="module", autouse=True)
def check_download():
    check_file_task()


def picture2words():
    """截图返回文字"""
    save_path = current_directory + os.sep + 'screenshot.png'
    screenshot = pyautogui.screenshot()  
    screenshot.save(save_path) 
    # 预处理图片
    img = cv2.imread(save_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(save_path, thresh_img)
    # win32gui.EnumWindows(enum_windows_proc, None)
    """
    窗口句柄: 11931444, 窗口标题: Fairy Auto, 窗口类：Qt672QWindowIcon
    窗口句柄: 1641340, 窗口标题: 绝区零, 窗口类：UnityWndClass
    """
    # input()
    ocr = PaddleOCR(use_angle_cls=True)
    res = ocr.ocr(save_path.replace('.jpg', '2.jpg'))
    info = {}
    print(res)
    for line in res:
        for data in line:
            info[data[1][0].strip()] = data[1][1]
    os.remove(save_path)
    print(info)
    return info


def compare_info(info, s):
    """匹配Info的key, 并返回key"""
    key = []
    for k in info.keys():
        if re.search(s, k) is not None and info[k]>0.9:
            key.append(k)
    return key


def enum_windows_proc(hwnd, lParam):  
    # lParam 是一个额外的参数，你可以通过调用 EnumWindows 传递给它  
    # 在这个例子中，我们不会使用它，所以简单地将其忽略  
    # 获取窗口标题  
    window_title = win32gui.GetWindowText(hwnd)
    window_class = win32gui.GetClassName(hwnd)  
    # 如果窗口标题不为空，则打印它（可选）  
    if window_title:  
        print(f"窗口句柄: {hwnd}, 窗口标题: {window_title}, 窗口类：{window_class}")   
    # 返回True以继续枚举  
    return True 


class TestGui:
    def page_redirection(self, window, dst_page):
        button = window.navigationInterface.items.get(dst_page)
        QTest.mouseClick(button, Qt.MouseButton.LeftButton)
        QTest.qWait(3000)
    
    def get_cur_widge_name(self, obj):
        return obj.stackedWidget.currentWidget().objectName()
         
    def screenshot_and_compare(self, s):
        info = picture2words()
        key = compare_info(info, s)
        return key

    def get_widget_global_pos(self, widget: QWidget):
        x, y, w, h = widget.pos().x(), widget.pos().y(), widget.geometry().width(), widget.geometry().height()
        parent = widget.parent()
        while parent is not None:
            x += parent.pos().x()
            y += parent.pos().y()
            parent = parent.parent()
        return x+w/2,y+h/2

    def widget_click(self, widget: QWidget):
        x, y = self.get_widget_global_pos(widget)
        pyautogui.click(x, y)
        QTest.qWait(1000)

    def fight_edit(self, window, action, data):
        """编辑战斗设计"""
        self.page_redirection(window, FIGHTEDIT)
        pass

    def analysize_dom(self, dom: Dom, s):
        if s[:3] != "dom":
            return s
        datas = s.split('.')[1:]
        res = dom
        for data in datas:
            if data.isdigit():
                res = res[int(data)]
            elif not data.isdigit() and type(res) == dict:
                res = res.get(data)
            else:
                res = getattr(res, data)  
        return res

    @pytest.mark.parametrize("testcase", load_testcase())
    # @pytest.mark.parametrize("testcase", load_one_testcase("home.yaml"))
    def test_cases(self, window, testcase):
        try:
            f12 = False
            window, dom = window
            des, steps, assert_ = testcase["des"], testcase["steps"], testcase["assert_"]
            print(des)
            for step in steps:
                func_n = step[0]
                params = step[1:]
                kwargs = {}
                for param in params:
                    k, v = param.split("=")
                    v_dom = self.analysize_dom(dom, v)
                    kwargs[k] = v_dom
                    if "task" in param:
                        f12 = True
                func = getattr(self, func_n)
                func(**kwargs)
            func_n, param, assert_data = assert_[0], assert_[1], assert_[-1]
            func = getattr(self, func_n)
            if param and assert_data:
                k, v = param.split('=')
                kwargs = {k: self.analysize_dom(dom, v)}
                assert func(**kwargs) == self.analysize_dom(dom, assert_data)
            elif not param and assert_data:
                assert func() == self.analysize_dom(dom, assert_data)
            elif param and not assert_data:
                k, v = param.split('=')
                kwargs = {k: self.analysize_dom(dom, v)}            
                assert func(**kwargs)
            else:
                assert func() 
        finally:
            if f12:
                pyautogui.press('f12') 
                rightbottom = (window.pos().x()+window.size().width()-10, window.pos().y()+window.size().height()-10)
                print(rightbottom)
                pyautogui.moveTo(rightbottom[0], rightbottom[1])
                QTest.qWait(1000)
                pyautogui.click(rightbottom[0], rightbottom[1])

    # def test_yincang(self, window):
    #     window, _ = window
    #     rightbottom = (window.pos().x()+window.size().width()-10, window.pos().y()+window.size().height()-10)
    #     print(rightbottom)
    #     pyautogui.moveTo(rightbottom[0], rightbottom[1])
    #     QTest.qWait(1000)
    #     pyautogui.click(rightbottom[0], rightbottom[1])     
    #     input()
    # @pytest.mark.parametrize("action,data", [
    #     [("edit", ("青衣", "e", "press", 0.3, 0.1, 3)),
    #      ("add", ("青衣", "e", "press", 0.3, 0.1, 3)),
    #      ("save", ()),
    #     ]
    # ])
    # def test_fightedit_page(self, window, action, data):
    #     _, p = self.window_analyze(window)
    #     print(p[FIGHTEDIT])
    #     self.page_redirection(window, FIGHTEDIT)
        
        
