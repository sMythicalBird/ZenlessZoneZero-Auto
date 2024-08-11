from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


class InfoBarUtils:

    @staticmethod
    def show_info_bar_not_config(parent):
        InfoBar.warning(
            title="暂未配置,请您先进行配置",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=parent
        )

    @staticmethod
    def start_success(parent):
        InfoBar.success(
            title=parent.tr('启动成功(＾∀＾●)'),
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent
        )

    @staticmethod
    def start_fail(parent):
        InfoBar.warning(
            title=parent.tr('启动失败(╥╯﹏╰╥)'),
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=parent
        )

    @staticmethod
    def start_error(parent):
        InfoBar.error(
            title="启动游戏时发生错误",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=parent
        )

    @staticmethod
    def is_running_Synthesis(parent):
        InfoBar.warning(
            title="正在合成，请勿重复运行",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent
        )

    @staticmethod
    def show_info_bar_success_config(parent):
        InfoBar.success(
            title="配置成功，准备进行合成",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=parent
        )

    @staticmethod
    def success_config_boss_running(parent):
        InfoBar.success(
            title="配置成功，准备运行",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=parent
        )

    @staticmethod
    def show_info_bar(parent):
        InfoBar.error(
            title="请选择项目根路径【基础配置】",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent,
        )

    @staticmethod
    def update_success(parent):
        InfoBar.success(
            # 提示信息的内容，告知用户更新成功
            title=parent.tr('修改成功'),
            content="",
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=parent.display_value_position,
        )

    @staticmethod
    def update_fail(parent):
        InfoBar.error(
            title=parent.tr('修改失败'),
            content="",
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=parent.display_value_position,
        )

    @staticmethod
    def choose_root_path(parent):
        InfoBar.error(
            title=parent.tr('请选择项目根路径'),
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent.infoBarPosition,
        )

    @staticmethod
    def is_running_boss_task(parent):
        InfoBar.warning(
            title="Boss任务正在运行，请勿重复运行",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent
        )

    @staticmethod
    def is_blank_boss_list(parent):
        InfoBar.warning(
            title="请选择Boss",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent
        )

    @staticmethod
    def is_stop_boss_task(parent):
        InfoBar.success(
            title="Boss任务已停止",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=parent
        )

    @staticmethod
    def is_stop_synthesis_task(parent):
        InfoBar.success(
            title="合成任务已停止",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=parent
        )

    @staticmethod
    def is_wait_stop_boss_task(parent):
        InfoBar.warning(
            title="等待中......Boss停止",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=parent
        )

    @staticmethod
    def is_not_boss_task(parent):
        InfoBar.warning(
            title="暂未运行",
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=parent
        )
