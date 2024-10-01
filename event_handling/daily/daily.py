import time, datetime

from utils.task import task_daily as task
from utils import control, logger
from schema import Position
from utils import screenshot
from re import Pattern, template
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Callable, Any, Dict, Union


# 点击进入游戏
@task.page(name="点击进入游戏", target_texts=["点击进入游戏"])
def action(positions: Dict[str, Position]):
    pos = positions.get("点击进入游戏")
    # logger.debug(f"坐标: {pos}")
    control.click(pos.x, pos.y)
    time.sleep(0.1)


# 领取月卡
@task.page(name="月卡", target_texts=["今日到账"])
def action(positions: Dict[str, Position]):
    pos = positions.get("今日到账")
    control.click(pos.x, pos.y)
    time.sleep(1)
    control.press("esc", duration=0.1)
    time.sleep(1)


# 活跃度已满，退出
@task.page(
    name="活跃度已满",
    target_texts=["活跃度已满", "·活跃度已满", "●活跃度已满"],
    priority=6,
)
def action(positions: Dict[str, Position]):
    logger.info("活跃度已满，退出")
    task.stop()
    # TODO 如何保证识别到活跃度已满后退出脚本执行？


# 点击快捷手册
@task.page(name="更多", target_texts=["私信", "快捷手册", "成就"])
def action(positions: Dict[str, Position]):
    pos = positions.get("快捷手册")
    # logger.debug(f"坐标: {pos}")
    control.click(pos.x, pos.y)
    time.sleep(1)


# 点击日常
@task.page(name="点击日常", target_texts=["目标", "日常", "训练", "挑战"])
def action(positions: Dict[str, Position]):
    pos = positions.get("日常")
    # logger.debug(f"坐标: {pos}")
    control.click(pos.x, pos.y)
    time.sleep(1)


# 没东西就一直esc
@task.page(name="返回主界面", priority=0)
def action():
    control.esc()
    time.sleep(1)


@task.page(
    name="日常任务执行",
    target_texts=["前往", "进行中"],
    exclude_texts=["活跃度已满", "·活跃度已满", "●活跃度已满"],
    priority=6,
)
def action():
    logger.debug("日常任务执行页面")
    test()


class DailyTask:
    def __init__(self) -> None:
        # path = r'D:\ZZZ-Auto\dev\ZenlessZoneZero-Auto\test\screenshots\daily_task_20240908-110003.377.png'
        # self.img_BGR = cv2.imread(path)
        # self.screen = cv2.cvtColor(self.img_BGR, cv2.COLOR_BGR2RGB)
        self.tasks_titles = [
            "品尝1次咖啡",
            "去报刊亭刮卡签到",
            "开启今日录像店经营",
        ]  # 日常任务名称
        self.unfinished_text = "进度：0/1"
        self.goto_text = "前往"

        self.ocr_targets = []
        for i in self.tasks_titles:
            self.ocr_targets.append(i)
        self.ocr_targets.append(self.unfinished_text)
        self.ocr_targets.append(self.goto_text)

        self.daily_tasks = {}
        self.coffee_prefers = ["汀曼特调", "参汤黑咖", "新艾利都特调"]  # 咖啡偏好

        self.open_shop_charactors = ["简", "猫又"]  # 开启今日录像店经营角色名

    def gen_daily_task_list(
        self, ocr_results=None
    ):  # 生成日常任务列表，返回包含任务名称、文字位置、点击位置的字典
        if ocr_results is None:
            ocr_results = task.ocr(screenshot())
        # print(f"----------------↓-ocr_results-↓----------------")
        # for i in ocr_results:
        #     if i.text in self.ocr_targets:
        #         print(i.text, i.position)
        # print(f"----------------↑-ocr_results-↑----------------\n")

        if self.detect_text_in_ocr_results(
            "活跃度已满", ocr_results
        ):  # 检测日常是否完成
            logger.info("日常任务已完成")
            return None
        else:
            for task_name in self.tasks_titles:
                if self.detect_text_in_ocr_results(task_name, ocr_results):
                    for i in [x for x in ocr_results if task_name in x.text]:
                        self.daily_tasks[task_name] = {}
                        self.daily_tasks[task_name]["text_pos"] = i.position
                    # if task_name == self.tasks_titles[2]:  # 录像店经营日常单独判断，1.2更新后无需单独处理
                    #     self.daily_tasks[task_name]["finished"] = self.check_open_shop_finished(ocr_results)

                    # else:
                    #     self.daily_tasks[task_name]["click_pos"] = self.get_click_position(task_name, ocr_results)

                    self.daily_tasks[task_name]["click_pos"] = self.get_click_position(
                        task_name, ocr_results
                    )

        return self.daily_tasks

    def get_click_position(
        self, task_name, ocr_results
    ) -> Optional[Position]:  # 获取任务“前往”按钮点击位置
        # if task_name is not self.tasks_titles[2]:  # 录像店经营日常无前往按钮
        #     for i in [x for x in ocr_results if self.goto_text in x.text]:
        #         if (
        #             i.position.x >= self.daily_tasks[task_name]["text_pos"].x1
        #             and i.position.x <= self.daily_tasks[task_name]["text_pos"].x2
        #         ):
        #             click_pos = i.position
        #             break
        #         else:
        #             click_pos = None
        #     return click_pos

        for i in [x for x in ocr_results if self.goto_text in x.text]:
            if (
                i.position.x >= self.daily_tasks[task_name]["text_pos"].x1
                and i.position.x <= self.daily_tasks[task_name]["text_pos"].x2
            ):
                click_pos = i.position
                break
            else:
                click_pos = None

        return click_pos

    # def check_open_shop_finished(self, ocr_results) -> bool|None:  # 检测开启今日录像店经营状态，1.2更新后无需单独处理
    #     if self.detect_text_in_ocr_results(self.tasks_titles[2], ocr_results):
    #         for i in [x for x in ocr_results if self.unfinished_text in x.text]:
    #             if (
    #                 i.position.x >= self.daily_tasks[self.tasks_titles[2]]["text_pos"].x1
    #                 and i.position.x <= self.daily_tasks[self.tasks_titles[2]]["text_pos"].x2
    #             ):
    #                 open_shop_finished = False
    #                 break
    #             else:
    #                 open_shop_finished = True
    #         return open_shop_finished
    #     else:
    #         return None

    @staticmethod
    def detect_text_in_ocr_results(
        text, ocr_results
    ) -> bool:  # 检测文本是否包含在ocr结果字符串中
        if len([x for x in ocr_results if text in x.text]) > 0:
            return True
        else:
            return False

    @staticmethod
    def to_daily_menu() -> None:  # 进入“快捷手册-日常”界面
        while True:
            ocr_results = task.ocr(screenshot())
            # print(ocr_results)
            if "日常" not in [x.text for x in ocr_results]:  # 检测“日常”文本
                if "快捷手册" not in [
                    x.text for x in ocr_results if x.position.y > 680
                ]:  # 检测下方“快捷手册”文本
                    control.press("esc", duration=0.1)
                    time.sleep(0.5)
                else:
                    click_pos = [
                        x.position for x in ocr_results if "快捷手册" in x.text
                    ][0]
                    control.click(click_pos.x, click_pos.y, duration=0.1)
                    time.sleep(0.5)
            else:
                click_pos = [x.position for x in ocr_results if "日常" in x.text][0]
                control.click(click_pos.x, click_pos.y, duration=0.1)
                time.sleep(0.5)
                logger.info("进入日常界面")
                break

    def to_normal_screen(self) -> None:  # 返回到普通界面
        flag = True
        times = 0
        while flag and times < 5:
            ocr_results = task.ocr(screenshot())
            # print(times)
            if self.detect_text_in_ocr_results("星期", ocr_results):  # 检测星期文本
                flag = False
                logger.info("返回到普通界面")
                break
            else:
                control.press("esc", duration=0.1)
                time.sleep(1.2)
                times += 1

    @staticmethod
    def click_to_pass() -> None:  # 点击"跳过"或"确认"或"确定"
        pass_list = ["跳过", "确认", "确定"]
        ocr_results = task.ocr(screenshot())
        for i in pass_list:
            if i in [x.text for x in ocr_results]:
                click_pos = [x for x in ocr_results if x.text == i][0].position
                control.click(click_pos.x, click_pos.y)
                time.sleep(1)
                break

    def daily_task_coffee(self) -> None:  # 品尝1次咖啡
        click_pos = self.daily_tasks["品尝1次咖啡"]["click_pos"]
        control.click(click_pos.x, click_pos.y)
        time.sleep(1)
        self.click_to_pass()  # 确认传送
        time.sleep(1.5)  # 画面切换加载时间较长
        # control.press("F", duration=0.1)  # 1.2更新后无需点击F键
        # time.sleep(1)

        ocr_results = task.ocr(screenshot())
        coffee_list = [
            x for x in ocr_results if x.position.x < 750 and x.position.y > 420
        ]

        def selete_coffee():  # 根据self.coffee_prefers选择咖啡
            default_click_pos = Position(
                x1=125, y1=557, x2=179, y2=572
            )  # 默认选择第一个咖啡
            click_pos = None
            for j in self.coffee_prefers:
                for i in coffee_list:
                    # print(j, i.text)
                    if j in i.text:
                        click_pos = i.position
                        logger.info(f"选择{j}@({click_pos.x},{click_pos.y})")
                        break
                if click_pos is not None:
                    break

            if click_pos is None:
                return default_click_pos
            else:
                return click_pos

        click_pos = selete_coffee()
        control.click(click_pos.x, click_pos.y)
        time.sleep(1)

        click_pos = [x for x in ocr_results if x.text == "点单"][
            0
        ].position  # 点单按钮位置（点单后无确认按钮）
        control.click(click_pos.x, click_pos.y)
        time.sleep(1)

        for i in range(2):  # 点单后1次跳过，1次确认
            self.click_to_pass()
            time.sleep(1)

        return

    def daily_task_scratch(self) -> None:  # 报刊亭刮卡签到

        def scratch_card():
            points = [
                (550, 380),
                (750, 380),
                (550, 400),
                (750, 400),
                (550, 420),
                (750, 420),
                (550, 440),
                (750, 440),
            ]  # 报刊亭刮卡

            for i in range(len(points) - 1):
                control.move_at(
                    points[i][0], points[i][1], points[i + 1][0], points[i + 1][1]
                )
                time.sleep(0.3)

        click_pos = self.daily_tasks["去报刊亭刮卡签到"]["click_pos"]
        control.click(click_pos.x, click_pos.y)
        time.sleep(1)
        self.click_to_pass()  # 确认传送
        time.sleep(1.5)  # 画面切换加载时间较长

        # control.press("W", duration=0.5)
        # time.sleep(1)
        # control.press("F", duration=0.1)
        # time.sleep(1.5)

        ocr_results = task.ocr(screenshot())
        click_pos = [x for x in ocr_results if x.text == "刮刮卡"][0].position
        # print(click_pos.x, click_pos.y)

        control.click(click_pos.x, click_pos.y)
        time.sleep(1.5)

        scratch_card()  # 刮卡
        time.sleep(1.5)
        self.click_to_pass()  # 确认
        time.sleep(1)
        return

    def daily_task_open_shop(self) -> None:  # 开启今日录像店经营
        # time.sleep(1)
        # self.to_normal_screen()  # 返回到普通界面
        # time.sleep(1)

        # control.press("M", duration=0.1)  # 打开传送界面
        # time.sleep(0.5)

        # for i in range(9):  # 切换到录像店传送界面
        #     ocr_results = task.ocr(screenshot()[400:480, 420:840, :])
        #     if "Random Play" not in [x.text for x in ocr_results]:
        #         control.click(360, 300)
        #         time.sleep(1)
        #     else:
        #         break

        # ocr_results = task.ocr(screenshot())
        # click_pos = [x for x in ocr_results if x.text == "柜台"][0].position  # 点击柜台
        # control.click(click_pos.x, click_pos.y)
        # time.sleep(1)
        # self.click_to_pass()
        # time.sleep(1.5)  # 等待场景切换加载时间

        # control.move_rel(120, 0)  # 旋转镜头，对准邦布
        # time.sleep(0.5)
        # control.press("W", duration=0.3)
        # time.sleep(0.5)
        # control.press("F", duration=0.1)
        # time.sleep(2)

        click_pos = self.daily_tasks["开启今日录像店经营"]["click_pos"]
        control.click(click_pos.x, click_pos.y)
        time.sleep(1)
        self.click_to_pass()  # 确认传送
        time.sleep(1.5)  # 画面切换加载时间较长

        while True:
            time.sleep(0.5)
            ocr_results = task.ocr(screenshot())
            if "昨日账本" in [x.text for x in ocr_results]:
                control.click(900, 160, duration=0.1)  # 点击红色关闭按钮
                break
        time.sleep(1)

        ocr_results = task.ocr(screenshot())
        if "选择宣传员" in [x.text for x in ocr_results]:
            click_pos = [x for x in ocr_results if x.text == "选择宣传员"][0].position
            control.click(click_pos.x, click_pos.y + 110)
        else:
            control.click(600, 500)
        time.sleep(1)

        characters = self.open_shop_charactors
        today = datetime.date.today()
        ocr_results = task.ocr(screenshot())
        ocr_results = [
            x for x in ocr_results if x.position.x1 > 350
        ]  # 过滤掉左侧干员介绍文本
        if today.timetuple().tm_yday % 2 == 0:  # 奇偶数日轮换角色
            if characters[0] in [x.text for x in ocr_results]:
                click_pos = [x for x in ocr_results if x.text == characters[0]][
                    0
                ].position
                control.click(click_pos.x, click_pos.y)
            else:
                control.click(420, 180)  # 点击第一个角色
        else:
            if characters[1] in [x.text for x in ocr_results]:
                click_pos = [x for x in ocr_results if x.text == characters[1]][
                    0
                ].position
                control.click(click_pos.x, click_pos.y)
            else:
                control.click(560, 180)  # 点击第二个角色
        self.click_to_pass()
        time.sleep(1)

        ocr_results = task.ocr(screenshot())
        click_pos_start = [x for x in ocr_results if x.text == "开始营业"][0].position
        control.click(click_pos_start.x, click_pos_start.y - 100)
        time.sleep(1)

        ocr_results = task.ocr(screenshot())
        click_pos_recommend = [x for x in ocr_results if x.text == "推荐上架"][
            0
        ].position
        click_pos_on_shelves = [x for x in ocr_results if x.text == "上架"][0].position
        control.click(click_pos_recommend.x, click_pos_recommend.y)
        time.sleep(1)
        control.click(click_pos_on_shelves.x, click_pos_on_shelves.y)
        time.sleep(1)
        control.click(click_pos_start.x, click_pos_start.y)
        time.sleep(1)

        for i in range(2):
            self.click_to_pass()
            time.sleep(1)
        control.press("esc", duration=0.1)


dailytask = DailyTask()


def test():
    daily_task_finished = False
    while daily_task_finished is False:
        dailytask.to_daily_menu()
        tasklist = dailytask.gen_daily_task_list()
        print(tasklist)

        for task_name, task_info in tasklist.items():
            if task_name == "品尝1次咖啡" and task_info["click_pos"] is not None:
                dailytask.daily_task_coffee()
                continue
            elif task_name == "去报刊亭刮卡签到" and task_info["click_pos"] is not None:
                dailytask.daily_task_scratch()
                continue
            # elif task_name == "开启今日录像店经营" and task_info["finished"] is False:
            elif (
                task_name == "开启今日录像店经营" and task_info["click_pos"] is not None
            ):
                dailytask.daily_task_open_shop()
            else:
                daily_task_finished = True
                logger.info(f"日常任务已完成")


test()
