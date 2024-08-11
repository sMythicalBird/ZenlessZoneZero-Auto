import json
import os

from PySide6.QtCore import QObject, Signal, QFileSystemWatcher


# 配置文件路径
# config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
#                          'AppData', 'config.json')


class ConfigWatcher(QObject):
    """
    监视配置文件变动的类。

    当配置文件发生变化时，通过configChanged信号通知监听者。
    """

    # 定义一个信号，用于在配置文件发生变化时发出通知
    configChanged = Signal()

    def __init__(self,config_path):
        """
        初始化ConfigWatcher类实例。

        参数:
        - config_path: 配置文件的路径，将对此路径进行监视以检测变化。
        """
        super().__init__()
        self.config_path = config_path
        # 初始化文件系统监视器
        self.watcher = QFileSystemWatcher(self)
        # 将配置文件路径添加到监视器中
        self.watcher.addPath(self.config_path)
        # 当文件发生变化时，连接到on_file_changed方法
        self.watcher.fileChanged.connect(self.on_file_changed)

    def on_file_changed(self, path):
        """
        当监视的文件发生变化时调用的方法。

        参数:
        - path: 发生变化的文件路径。

        如果发生变化的文件是config.json，則发出configChanged信号。
        """
        # 检查变化的文件是否是config.json
        if path.endswith(self.config_path):
            # 如果是，发出configChanged信号
            self.configChanged.emit()
