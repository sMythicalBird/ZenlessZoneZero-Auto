# -*- coding: utf-8 -*-
"""
@file: fight_edit_interface.py
@time: 2024/8/12
@auther: sMythicalBird
"""
from PySide6.QtGui import QIcon
from qfluentwidgets import ScrollArea
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QSizePolicy
    
)

from PySide6.QtCore import Qt
from qfluentwidgets import ComboBox, VBoxLayout, PushButton, TitleLabel, BodyLabel, SpinBox, ExpandGroupSettingCard, FluentIcon, LineEdit, DoubleSpinBox, ScrollArea
from qfluentwidgets.common.icon import FluentIcon as FIF
import yaml

class FightEditInterface(ScrollArea):
    def __init__(self):
        super().__init__()
        self.setObjectName("FightEditInterface")
        # 添加窗口和布局
        self.view = QWidget(self)
        # 给view设置布局
        self.vBoxLayout = VBoxLayout(self.view)
        self.BattleSettingWidget()
        self.init_ui()
    
    def BattleSettingWidget(self):
        self.Expand_Card = ExpandGroupSettingCard(FluentIcon.SETTING, "战斗设置", "自定义你的战斗")

        # 键位设置
        self.Keyboard_Label = BodyLabel("按下按键")
        self.Keyboard_Entry = LineEdit()
        self.Keyboard_Entry.setFixedWidth(200)
        # 按键选项
        self.Action_Label = BodyLabel("按键选项")
        self.Action_ComboBox = ComboBox()
        self.Action_ComboBox.addItems(['press', 'down', 'up'])
        self.Action_ComboBox.setFixedWidth(200)
        # 持续时间
        self.Duraction_Label = BodyLabel("持续时间")
        self.Duraction_Spinbox = DoubleSpinBox()
        self.Duraction_Spinbox.setRange(0, 100)
        self.Duraction_Spinbox.setValue(1)
        self.Duraction_Spinbox.setFixedWidth(200)
        # 间隔时间
        self.Delay_Label = BodyLabel("间隔时间")
        self.Delay_Spinbox = DoubleSpinBox()
        self.Delay_Spinbox.setRange(0, 100)
        self.Delay_Spinbox.setValue(1)
        self.Delay_Spinbox.setFixedWidth(200)
        # 重复次数
        self.Repeat_Label = BodyLabel("重复次数")
        self.Repeat_Spinbox = SpinBox()
        self.Repeat_Spinbox.setRange(0, 100)
        self.Repeat_Spinbox.setValue(1)
        self.Repeat_Spinbox.setFixedWidth(200)

        # 监听数值改变信号
        self.Duraction_Spinbox.valueChanged.connect(lambda value: print("当前值：", value))

        # 添加 ExpandCard 的组件
        self.add(self.Keyboard_Label, self.Keyboard_Entry)
        self.add(self.Action_Label, self.Action_ComboBox)
        self.add(self.Duraction_Label, self.Duraction_Spinbox)
        self.add(self.Delay_Label, self.Delay_Spinbox)
        self.add(self.Repeat_Label, self.Repeat_Spinbox)
        
        return self.Expand_Card
        
       

    def add(self, label, widget):
        self.w = QWidget()
        self.w.setFixedHeight(60)

        self.layout = QHBoxLayout(self.w)
        self.layout.setContentsMargins(48, 12, 48, 12)

        self.layout.addWidget(label)
        self.layout.addStretch(1)
        self.layout.addWidget(widget)

        # 添加组件到设置卡
        self.Expand_Card.addGroupWidget(self.w)
    # 仅为测试, 事实上, 每一个 ExpandCard 的内容要被做成字典然后添加到一个列表中, 再导出    
    # def export_yaml(self):
    #     data = {
    #         "key": self.Keyboard_Entry.text(),
    #         "duraction": self.Duraction_Spinbox.value(),
    #         "delay": self.Delay_Spinbox.value(),
    #         "repeat": self.Repeat_Spinbox.value()
    #     }

    #     yaml_data = yaml.dump([data], allow_unicode=True)
    #     print(yaml_data)

    def get_contents(self):
        return {
            "key": self.Keyboard_Entry.text(),
            "duraction": self.Duraction_Spinbox.value(),
            "delay": self.Delay_Spinbox.value(),
            "repeat": self.Repeat_Spinbox.value()
        }

    def init_ui(self):
        # 创建主布局为竖向布局
        self.main_layout = VBoxLayout(self)
        # 设置排布方式为向上排布
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Widget 控件可被拉伸
        self.setWidgetResizable(True)

        # 创建容器和布局，用于放置可滚动的内容
        self.container_widget = QWidget()
        # 创建容器内的竖向布局
        self.container_layout = VBoxLayout(self.container_widget)
        # 设置为向上排布
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # 中间间隔 10 像素
        self.container_layout.setSpacing(10)
        # 设置容器的主布局为 container_layout
        self.container_widget.setLayout(self.container_layout)
        # 配置布局填充模式为填满
        self.container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 将view设为中心部件
        self.setWidget(self.container_widget)
        # 设置填充模式为填满
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 将容器设置为滑动区域的中心部件
        # scroll_area.setWidget(container_widget)
        # scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 添加标题为 战斗设计
        self.titlebar = TitleLabel("战斗设计")
        # 添加到容器布局
        self.container_layout.addWidget(self.titlebar)

        # 配置选择角色框
        self.character_combobox = ComboBox()
        # 设置下拉框内容
        self.character_combobox.addItems(['朱鸢', '安比', '妮可'])
        # 在容器内绘制
        self.container_layout.addWidget(self.character_combobox)
        self.character_combobox.setFixedHeight(40)

        # 创建自定义控件
        self.fight_1 = self.BattleSettingWidget()
        self.fight_2 = self.BattleSettingWidget()

        self.container_layout.addWidget(self.fight_1)
        self.container_layout.addWidget(self.fight_2)
        self.container_layout.addStretch()

        
        

        

    