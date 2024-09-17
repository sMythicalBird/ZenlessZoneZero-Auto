import time, datetime

from utils.task import task_daily as task
from utils import control, logger
from schema import Position
from utils import screenshot
from re import Pattern,template
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
@task.page(name="活跃度已满", target_texts=["活跃度已满", "·活跃度已满"], priority=9)
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


@task.page(name="日常任务执行", target_texts=["前往", "进行中"], priority=6)
def action():
    logger.debug("日常任务执行页面")
    daily_task()


def daily_task() -> None:
    ocr_results = task.ocr(screenshot())
    task_list_title = ["去报刊亭刮卡签到", "品尝1次咖啡", "开启今日录像店经营"]    
    # finished_text = "进度：1/1"
    unfinished_text = "进度：0/1"
    goto_text = "前往"
    # progressing_text = "进行中"

    ocr_target_list = [] # 识别目标文本列表

    for i in task_list_title:
        ocr_target_list.append(i)

    ocr_target_list.append(unfinished_text)
    ocr_target_list.append(goto_text)
    
    ocr_target_pos_list = [] # 识别目标位置列表

    for ocr_result in ocr_results:
        if ocr_result.text in ocr_target_list:
            ocr_target_pos_list.append(ocr_result)
            
    daily_tasks = {} # 日常任务对应文本坐标字典

    for title in task_list_title:
        for ocr_target in ocr_target_pos_list:
            if ocr_target.text == title:
                daily_tasks[title] = ocr_target.position

    def get_click_pos(title): # 获取任务对应点击位置
        for i in [x for x in ocr_results if x.text == goto_text]:
            if i.position.x1 > daily_tasks[title].x1 and i.position.x1 < daily_tasks[title].x2:
                return i.position

    def click_to_pass(): # 点击"跳过"或"确认"或"确定"
        time.sleep(1)
        pass_list = ["跳过", "确认", "确定"]
        ocr_results = task.ocr(screenshot())
        for i in pass_list:
            if i in [x.text for x in ocr_results]:
                click_pos = [x for x in ocr_results if x.text == i][0].position
                control.click(click_pos.x, click_pos.y)
                time.sleep(1)

    def daily_task_coffee(): # 品尝1次咖啡
        click_pos = get_click_pos(task_list_title[1])
        control.click(click_pos.x, click_pos.y)
        click_to_pass()
        time.sleep(1)
        control.press("F", duration=0.1)
        time.sleep(2)

        ocr_results = task.ocr(screenshot())
        if "点单" in [x.text for x in ocr_results]:            
            if "新艾利都特调" in [x for x in ocr_results if x.position.x < 750 and x.position.y > 420]: # 过滤掉右侧咖啡效果介绍
                click_pos = [x for x in ocr_results if x.text == "新艾利都特调"][0].position
                control.click(click_pos.x, click_pos.y - 30)
            else:
                control.click(152, 535) # 点击第一个咖啡            
            time.sleep(1)
            click_pos = [x for x in ocr_results if x.text == "点单"][0].position
            control.click(click_pos.x, click_pos.y)
            time.sleep(2)

            ocr_results = task.ocr(screenshot())
            if "咖啡不可贪杯哦～" in [x.text for x in ocr_results]:
                click_to_pass()
            else:
                for i in range(2):
                    click_to_pass()
            for i in range(3):
                control.press("esc", duration=0.1)
                time.sleep(1.5)            
            return

    def daily_task_scratch(): # 报刊亭刮卡签到
        click_pos = get_click_pos(task_list_title[0])
        control.click(click_pos.x, click_pos.y)
        click_to_pass()
        print(f"waiting 2 seconds")
        time.sleep(2)
        control.press("W", duration=0.5)
        time.sleep(1)
        control.press("F", duration=0.1)
        time.sleep(1.5)
        ocr_results = task.ocr(screenshot())
        click_pos = [x for x in ocr_results if x.text == "刮刮卡"][0].position
        print(click_pos.x, click_pos.y)
        control.click(click_pos.x, click_pos.y)
        time.sleep(1.5)
        control.move_at(550, 380, 750, 380)
        time.sleep(0.2)    
        control.move_at(750, 380, 550, 400)
        time.sleep(0.2)
        control.move_at(550, 400, 750, 400)
        time.sleep(0.2)
        control.move_at(750, 400, 550, 420)
        time.sleep(0.2)
        control.move_at(550, 420, 750, 420)
        time.sleep(0.2)
        control.move_at(750, 420, 550, 440)
        time.sleep(0.2)
        control.move_at(550, 440, 750, 440)
        time.sleep(0.2)
        click_to_pass()
        time.sleep(1)
        for i in range(3):
            control.press("esc", duration=0.1)
            time.sleep(1)
        return

    def daily_task_open_shop(): # 开启今日录像店经营
        control.press("esc", duration=0.1)
        time.sleep(0.5)

        control.press("M", duration=0.1)
        time.sleep(0.5)

        for i in range(9):
            orc_results = task.ocr(screenshot()[400:480, 420:840, :])
            if "Random Play" not in [x.text for x in orc_results]:
                control.click(360, 300)
                time.sleep(1)
            else:
                break

        orc_results = task.ocr(screenshot())
        click_pos = [x for x in orc_results if x.text == "柜台"][0].position
        control.click(click_pos.x, click_pos.y)
        click_to_pass()
        time.sleep(2)
        control.move_rel(150, 0)
        time.sleep(0.5)
        control.press("W", duration=0.3)
        time.sleep(0.5)
        control.press("F", duration=0.1)
        time.sleep(1)
        control.click(900, 160)
        time.sleep(1)
        ocr_results = task.ocr(screenshot())
        if "选择宣传员" in [x.text for x in ocr_results]:
            click_pos = [x for x in ocr_results if x.text == "选择宣传员"][0].position
            control.click(click_pos.x, click_pos.y + 110)
        else:
            control.click(600, 500) 
        time.sleep(1)
        characters = ["简", "猫又"] # 每日使用角色
        today = datetime.date.today()
        ocr_results = task.ocr(screenshot())
        ocr_results = [x for x in ocr_results if x.position.x1 > 350] # 过滤掉左侧干员介绍文本
        if today.timetuple().tm_yday % 2 == 0: # 奇偶数日轮换角色
            if characters[0] in [x.text for x in ocr_results]:
                click_pos = [x for x in ocr_results if x.text == characters[0]][0].position
                control.click(click_pos.x, click_pos.y)
            else:
                control.click(420, 180)  # 点击第一个角色
        else:
            if characters[1] in [x.text for x in ocr_results]:
                click_pos = [x for x in ocr_results if x.text == characters[1]][0].position
                control.click(click_pos.x, click_pos.y)
            else:
                control.click(560, 180) 
        click_to_pass()
        time.sleep(1)
        ocr_results = task.ocr(screenshot())
        click_pos_start = [x for x in ocr_results if x.text == "开始营业"][0].position
        control.click(click_pos_start.x, click_pos_start.y - 100)
        time.sleep(1)
        ocr_results = task.ocr(screenshot())
        click_pos_recommend = [x for x in ocr_results if x.text == "推荐上架"][0].position
        click_pos_on_shelves = [x for x in ocr_results if x.text == "上架"][0].position
        control.click(click_pos_recommend.x, click_pos_recommend.y)
        time.sleep(1)
        control.click(click_pos_on_shelves.x, click_pos_on_shelves.y)
        time.sleep(1)
        control.click(click_pos_start.x, click_pos_start.y)
        time.sleep(1)
        for i in range(2):
            click_to_pass()
            time.sleep(1)
        control.press("esc", duration=0.1)


    for processing_task in [x for x in ocr_target_pos_list if x.text == unfinished_text]:
        for daily_task in daily_tasks:
            if processing_task.position.x > daily_tasks[daily_task].x1 and processing_task.position.x < daily_tasks[daily_task].x2:                
                # TODO 执行完某一项具体的日常任务后，如何正确退出循环？退出action函数？执行下一轮的识别循环？
                if daily_task == task_list_title[0]:
                    print("daily_task_scratch")
                    daily_task_scratch()
                    return
                elif daily_task == task_list_title[1]:
                    print("daily_task_coffee")
                    daily_task_coffee()
                    return
                elif daily_task == task_list_title[2]:
                    print("daily_task_open_shop")
                    daily_task_open_shop()
                    return