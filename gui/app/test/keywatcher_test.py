# 假设这是你的配置文件路径
import os
import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication

from app.watcher.key_watcher import KeyAndValWatcher

# 项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 配置文件路径config.json
config_path = os.path.join(project_root, 'AppData', 'config.json')

# 创建一个应用程序实例
app = QApplication(sys.argv)

# 创建 ConfigWatcher 实例
config_watcher = KeyAndValWatcher(config_path, 'TargetMap', 'Zone')

@Slot(str, str, str)
def on_config_changed(group_name, key_name, new_value):
    print(f"配置文件中 {group_name} 组下的 {key_name} 键的值已更改为 {new_value}")

# 连接信号到槽函数
config_watcher.configChanged.connect(on_config_changed)

# 启动应用程序主循环
sys.exit(app.exec())