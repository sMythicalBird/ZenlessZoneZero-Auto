import json
import os
from PySide6.QtCore import QObject, Signal, QFileSystemWatcher
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class KeyAndValWatcher(QObject):
    """
    监视配置文件中特定组内键值变动的类。

    当指定的组内的键值发生变化时，通过configChanged信号通知监听者。
    """

    # 定义一个信号，用于在配置文件中的特定组内的键值发生变化时发出通知
    configChanged = Signal(str, str, str)  # 发出组名、键名和新的值

    class ConfigFileHandler(FileSystemEventHandler):
        def __init__(self, config_watcher):
            super().__init__()
            self.config_watcher = config_watcher

        def on_modified(self, event):
            if event.is_directory:
                return
            self.config_watcher.check_config_changes()

    def __init__(self, config_path, groupName, key_to_watch):
        """
        初始化ConfigWatcher类实例。

        参数:
        - config_path: 配置文件的路径，将对此路径进行监视以检测变化。
        - groupName: 需要监视的组名。
        - key_to_watch: 在指定组内需要监视的配置键。
        """
        super().__init__()
        self.config_path = config_path
        self.groupName = groupName
        self.key_to_watch = key_to_watch
        self.last_known_value = None  # 用于存储上一次已知的键值
        self.observer = Observer()  # 使用 watchdog 库来观察文件的变化

        # 初始化文件系统监视器
        self.handler = self.ConfigFileHandler(self)
        self.observer.schedule(self.handler, path=os.path.dirname(config_path), recursive=False)
        self.observer.start()

    def check_config_changes(self):
        """
        检查配置文件中的特定组内的键值是否发生了变化。
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                # 访问嵌套结构中的键值
                group_data = config_data.get(self.groupName, {})
                current_value = group_data.get(self.key_to_watch)
                if current_value != self.last_known_value:
                    self.last_known_value = current_value
                    self.configChanged.emit(self.groupName, self.key_to_watch, current_value)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def stop_watching(self):
        """
        停止监视文件的变化。
        """
        self.observer.stop()
        self.observer.join()
