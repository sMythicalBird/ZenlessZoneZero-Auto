import os
import subprocess
import winreg

from pylnk3 import Lnk
from qfluentwidgets import qconfig

from app.common.config import cfg
from app.utils.configUtils import json_file_path, get_compute_tactic


def update_game_path_from_config(program_config_path):
    """从给定的配置文件路径更新游戏路径"""
    # 检查配置文件路径是否存在
    if os.path.exists(program_config_path):
        # 打开配置文件，以读取模式
        with open(program_config_path, 'r', encoding='utf-8') as file:
            # 遍历文件的每一行
            for line in file.readlines():
                # 判断当前行是否是游戏安装路径配置行
                if line.startswith("game_install_path="):
                    # 提取路径并去除末尾的换行符或空格
                    game_path = line.split('=')[1].strip()
                    # 检查游戏路径是否存在
                    if os.path.exists(game_path):
                        # 如果路径存在，更新配置文件中的游戏路径
                        qconfig.set(cfg.game_path, os.path.abspath(os.path.join(game_path, "ZenlessZoneZero.exe")))
                        # 更新成功，返回True
                        return True
    # 配置文件路径不存在或游戏路径无效，返回False
    return False


def get_link_target(lnk_path):
    """
    获取快捷方式指向的目标路径。

    本函数尝试打开一个快捷方式文件，解析它指向的实际文件或目录，并返回该目标路径下的特定文件。

    参数:
    lnk_path -- 快捷方式的路径

    返回:
    如果成功解析快捷方式，则返回目标路径下的"config.ini"文件的完整路径。
    如果无法解析快捷方式或发生任何异常，则返回None。
    """
    try:
        # 以二进制模式打开快捷方式文件以进行读取
        with open(lnk_path, "rb") as lnk_file:
            # 解析快捷方式文件
            lnk = Lnk(lnk_file)
            # 返回快捷方式的工作目录下的"config.ini"文件路径
            return os.path.join(lnk.work_dir, "config.ini")
    except:
        # 如果发生任何异常，返回None
        return None


def detect_from_default_install_path():
    """从默认安装路径检测游戏配置文件路径"""
    default_config_path = os.path.join(os.getenv('ProgramFiles'), "Star Rail\\config.ini")
    return update_game_path_from_config(default_config_path)


def detect_from_start_menu():
    """从开始菜单的快捷方式检测游戏配置文件路径"""
    # 定义开始菜单中游戏快捷方式的路径
    start_menu_path = os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs",
                                   "米哈游启动器")
    # 构建游戏快捷方式文件的路径
    lnk_path = os.path.join(start_menu_path, "绝区零.lnk")
    # 通过快捷方式文件获取游戏配置文件路径
    program_config_path = get_link_target(lnk_path)
    # 如果获取到配置文件路径，则更新游戏路径配置；否则返回False
    return update_game_path_from_config(program_config_path) if program_config_path else False


def detect_from_hoyoplay():
    """从米哈游启动器检测游路径（占位）"""
    hoyoplay_default_path = os.path.join(os.getenv('ProgramFiles'), "miHoYo Launcher", "games", "ZenlessZoneZero Game",
                                         "ZenlessZoneZero.exe")
    if os.path.exists(hoyoplay_default_path):
        qconfig.set(cfg.game_path, (str)(os.path.abspath(hoyoplay_default_path)))
        return True
    return False


def open_registry_key(key_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        return key
    except FileNotFoundError:
        # print(f"未找到注册表路径'{key_path}'")
        pass
    except Exception as e:
        print(f"访问注册表错误: {e}")
    return None


def detect_register_from_install_path():
    key = None
    # 从注册表获取路径
    # 打开注册表项
    # key_path = r"Software\miHoYo\HYP\1_1\nap_cn"

    key_paths = [
        r"Software\miHoYo\HYP\1_1\nap_cn",
    ]

    for key_path in key_paths:
        key = open_registry_key(key_path)

        if key:
            try:
                # 读取安装路径
                install_path, _ = winreg.QueryValueEx(key, "GameInstallPath")
                if install_path:
                    # 构造完整的程序路径
                    program_path = os.path.join(
                        install_path, "ZenlessZoneZero.exe"
                    )
                    qconfig.set(cfg.game_path, (str)(program_path))
                    return True
            except Exception as e:
                # print(f"构建安装路径错误: {e}")
                pass
            finally:
                if "key" in locals():
                    key.Close()
    return None


detect_register_from_install_path()


def detect_game_path():
    """检测游戏路径，并更新配置，支持多种检测方式"""
    game_path = cfg.game_path.value
    if os.path.exists(game_path):
        return

    # 定义检测方式列表
    detection_methods = [detect_register_from_install_path, detect_from_default_install_path, detect_from_start_menu,
                         detect_from_hoyoplay]

    # 迭代执行每种检测方式，直到找到有效路径或尝试所有方式
    for method in detection_methods:
        if method():  # 如果检测成功，method() 返回 True，提前退出
            break


def auto_path_detection():
    if os.path.exists(json_file_path):
        if isinstance(get_compute_tactic(json_file_path, 'Program', 'AutoSetGamePath'), bool):
            return get_compute_tactic(json_file_path, 'Program', 'AutoSetGamePath')
