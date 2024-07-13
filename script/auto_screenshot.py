import time
from utils import RootPath, screenshot
from utils.task import task
from schema import Position
from typing import Dict
from utils import control, logger
from threading import Thread
from pynput.keyboard import Key, Listener
from PIL import Image
from random import choice


def key_event():
    def on_press(key):
        if key == Key.f12:
            task.stop()
            return False
        return None

    with Listener(on_press=on_press) as listener:
        listener.join()


key_thread = Thread(target=key_event)
key_thread.start()


@task.page(name="选择副本", target_text="作战机略", target_texts=["旧都列车"])
def select_map(positions: Dict[str, Position]):
    pos = positions.get("旧都列车")
    control.click(pos.x, pos.y)


@task.page(name="选择副本等级", target_texts=["外围$", "下一步"])
def select_level(positions: Dict[str, Position]):
    pos = positions.get("下一步")
    control.click(pos.x, pos.y)


@task.page(name="选择角色", target_texts=["出战"])
def select_role(positions: Dict[str, Position]):
    pos = positions.get("出战")
    control.click(pos.x, pos.y)


@task.page(
    name="格子地图",
    target_texts=["背包", "^当前层数"],
)
def grid_map():
    logger.debug("等待8秒后开始截图60张")
    time.sleep(8)
    screenshot_path = RootPath / "yolo/map/dataset/screenshot/自身位置"
    if not screenshot_path.exists():
        screenshot_path.mkdir()
    logger.debug(f"截图保存路径：{screenshot_path}")
    png_count = len(list(screenshot_path.glob("*.png")))
    if choice([True, False]):
        time.sleep(65)
    for i in range(10):
        screen = screenshot()
        screen = Image.fromarray(screen)
        screen.save(screenshot_path / f"{png_count+i}.png")
    control.esc()


@task.page(name="退出", target_texts=["^放弃$", "^暂离$"])
def exit_map(positions: Dict[str, Position]):
    pos = positions.get("^放弃$")
    control.click(pos.x, pos.y)


@task.page(name="确认退出", target_texts=["^确认$", "返回街区"])
def confirm_exit(positions: Dict[str, Position]):
    pos = positions.get("^确认$")
    control.click(pos.x, pos.y)


@task.page(name="结算界面", target_texts=["^完成$", "^执照等级$"])
def settle(positions: Dict[str, Position]):
    pos = positions.get("^完成$")
    control.click(pos.x, pos.y)


if __name__ == "__main__":
    task.run()
