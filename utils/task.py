# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: zzz.py
@time: 2024/7/5 下午11:44
@author SuperLazyDog
"""
import inspect
import time
from pathlib import Path
from re import Pattern, template
from typing import List, Optional, Callable, Any, Dict, Union
import numpy as np
from PIL import Image
from pydantic import BaseModel, Field, ConfigDict

from schema import Position, OcrResult
from schema.cfg.zero_info import state_zero
from .init import logger, RootPath
from .ocr import Ocr, paddle_ocr
from .utils import find_template, screenshot


class TextMatch(BaseModel):
    name: str | None = Field(None, title="文本匹配名称")
    text: str | Pattern = Field(title="文本")
    position: Position | None = Field(None, title="文本范围位置，(x1, y1, x2, y2)")

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if isinstance(self.text, str):  # 如果文本是字符串，则转换为正则表达式
            self.text = template(self.text)


class ImageMatch(BaseModel):
    name: str | None = Field(None, title="图片匹配名称")
    image: str | Path | np.ndarray = Field(title="图片")
    position: Position | None = Field(None, title="限定图片范围，(x1, y1, x2, y2)")
    confidence: float = Field(0.95, title="图片置信度", ge=0, le=1)

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        if isinstance(self.image, str):  # 如果图片是字符串则改为路径
            # 判断是否为绝对路径
            if not Path(self.image).is_absolute():
                if not self.image.endswith(".png"):
                    self.image += ".png"
                self.image = RootPath / "download" / self.image
        if isinstance(self.image, Path):
            if not self.image.exists():
                raise FileNotFoundError(f"图片路径不存在：{self.image}")
            self.name = self.name or self.image.stem
            self.image = np.array(Image.open(self.image))

    class Config:
        arbitrary_types_allowed = True


class Page(BaseModel):
    name: str = Field(None, title="页面名称")
    # 页面操作函数 函数参数为匹配到的目标位置或无参数，返回值为bool
    action: Union[Callable[[Dict[str, Position]], bool], Callable[[], bool]] = Field(
        title="页面操作函数"
    )
    targetTexts: List[TextMatch] = Field([], title="目标文本，匹配规则为与")
    excludeTexts: List[TextMatch] = Field([], title="排除目标文本，匹配规则为或")

    targetImages: List[ImageMatch] = Field([], title="目标图片，匹配规则为与")
    excludeImages: List[ImageMatch] = Field([], title="排除目标图片，匹配规则为或")

    matchPositions: Dict[str, Position] = Field(
        {},
        title="匹配位置，有名称目标图片或文本匹配成功后根据名称记录位置，没有名称则默认名称为 position'",
    )
    condition: Callable[[], bool] = Field(
        lambda: True, title="条件函数"
    )  # 条件函数 默认值为lambda表达式 返回True
    sleep: float = Field(1, title="页面操作函数执行后后等待时间，单位秒")
    priority: int = Field(5, title="页面优先级")

    def __init__(self, /, **data: Any):
        # 检查文本目标类型是否为字符串或正则表达式，如果是则转换为 TextMatch
        data["targetTexts"] = map(self.str2_text_match, data.get("targetTexts", []))
        data["excludeTexts"] = map(self.str2_text_match, data.get("excludeTexts", []))
        # 检查图片目标类型是否为字符串或图片，如果是则转换为 ImageMatch
        data["targetImages"] = map(self.str2_image_match, data.get("targetImages", []))
        data["excludeImages"] = map(
            self.str2_image_match, data.get("excludeImages", [])
        )
        super().__init__(**data)

    class Config:
        arbitrary_types_allowed = True

    def __call__(self, img: np.ndarray, ocrResults: List[OcrResult]) -> bool:
        """
        页面匹配
        :param img: 游戏画面截图
        :param ocrResults:  游戏画面识别结果
        :return:  bool
        """
        # 清空匹配位置
        if not self.condition():
            return False
        self.matchPositions = {}
        # 遍历目标文本 如果匹配到目标文本则记录位置 否则返回False
        for textMatch in self.targetTexts:
            if position := self.text_match(textMatch, ocrResults):
                self.matchPositions[textMatch.name or "position"] = position
            else:
                return False
        # 遍历排除文本 如果匹配到排除文本则返回False
        for textMatch in self.excludeTexts:
            if self.text_match(textMatch, ocrResults):
                return False
        # 遍历目标图片 如果匹配到目标图片则记录位置 否则返回False
        for imageMatch in self.targetImages:
            if position := self.image_match(imageMatch, img):
                self.matchPositions[imageMatch.name or "position"] = position
            else:
                return False
        # 遍历排除图片 如果匹配到排除图片则返回False
        for imageMatch in self.excludeImages:
            if self.image_match(imageMatch, img):
                return False
        return True

    @staticmethod
    def text_match(
        textMatch: TextMatch, ocrResults: List[OcrResult]
    ) -> Position | None:
        """
        文本匹配
        :param textMatch: 文本匹配
        :param ocrResults:  ocr 识别结果
        :return:
        """
        for ocr_result in ocrResults:
            if textMatch.text.search(ocr_result.text):
                # 如果文本位置不在指定范围内则继续
                if (
                    textMatch.position is not None
                    and ocr_result.position not in textMatch.position
                ):
                    continue
                return ocr_result.position
        return None

    @staticmethod
    def image_match(imageMatch: ImageMatch, img: np.ndarray) -> Position | None:
        """
        图片匹配
        :param imageMatch: 图片匹配
        :param img:  图片
        :return:
        """
        imgPosition = find_template(
            img, imageMatch.image, threshold=imageMatch.confidence
        )
        if imgPosition is not None:
            # 如果指定了图片位置范围且匹配位置不在范围内则返回None
            if (
                imageMatch.position is not None
                and imgPosition not in imageMatch.position
            ):
                return None
            return imgPosition

    @staticmethod
    def str2_text_match(text: str | Pattern | TextMatch) -> TextMatch:
        """
        检查文本目标类型是否为字符串或正则表达式，如果是则转换为 TextMatch
        """
        if isinstance(text, str) or isinstance(text, Pattern):
            name = text if isinstance(text, str) else text.pattern
            return TextMatch(name=name, text=text)
        return text

    @staticmethod
    def str2_image_match(image: str | Path | np.ndarray | ImageMatch) -> ImageMatch:
        """
        检查图片目标类型是否为字符串或图片，如果是则转换为 ImageMatch
        """
        if not isinstance(image, ImageMatch):
            return ImageMatch(image=image)
        return image


class ConditionalAction(BaseModel):
    name: str = Field(None, title="条件操作名称")
    condition: Callable[[], bool] = Field(title="条件函数")
    action: Callable[[], bool] = Field(title="操作函数列表")

    class Config:
        arbitrary_types_allowed = True

    def __call__(self) -> bool | None:
        if self.condition is None:
            raise Exception("条件函数未设置")
        if self.condition():
            return True
        else:
            return False


class _Task(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ocr: Ocr = Field(
        default_factory=Ocr,
        title="OCR识别器",
    )
    _pages: List[Page] = []  # title="函数列表", description="函数列表"
    _conditionalActions: list[ConditionalAction] = []  # title="条件操作函数列表"
    _running: bool = False  # title="是否运行中"
    _pause: bool = False  # title="是否暂停"
    lastPageName: str = ""  # title="上次页面名称"

    def page(
        self,
        name: str,
        priority: int = 5,
        target_text: str | Pattern | TextMatch = None,
        target_image: str | np.ndarray | ImageMatch = None,
        exclude_text: Optional[str | Pattern | TextMatch] = None,
        exclude_image: Optional[str | np.ndarray | ImageMatch] = None,
        target_texts: List[TextMatch | str | Pattern] = None,
        target_images: List[ImageMatch | str | np.ndarray] = None,
        exclude_texts: List[TextMatch | str | Pattern] = None,
        exclude_images: List[ImageMatch | str | np.ndarray] = None,
        condition: Callable[[], bool] = lambda: True,
        sleep: float = 1,
    ):
        """
        添加一个页面匹配任务 装饰器
        :param name: 页面名称
        :param priority: 页面优先级 默认值为0 越高越优先
        :param target_text: 目标文本 如果类型为str或Pattern则转换为TextMatch 名称为文本内容
        :param target_image: 目标图片 如果类型为str则转换为ImageMatch 名称为图片路径 如果类型为np.ndarray则转换为ImageMatch 将没有该目标位置
        :param exclude_text: 排除文本
        :param exclude_image: 排除图片
        :param target_texts: 目标文本列表 如果类型为str或Pattern则转换为TextMatch 名称为文本内容
        :param target_images: 目标图片列表 如果类型为str则转换为ImageMatch 名称为图片路径 如果类型为np.ndarray则转换为ImageMatch 将没有该目标位置
        :param exclude_texts: 排除文本列表
        :param exclude_images: 排除图片列表
        :param condition: 条件函数 默认值为lambda表达式 返回True
        :param sleep: 页面操作函数执行后后等待时间，单位秒
        :return: None
        """
        # 如果目标列表为None则转换为列表
        target_texts = target_texts or []
        target_images = target_images or []
        exclude_texts = exclude_texts or []
        exclude_images = exclude_images or []
        # 将 目标 添加到目标列表
        if target_text:
            target_texts += [target_text]
        if target_image:
            target_images += [target_image]
        if exclude_text:
            exclude_texts += [exclude_text]
        if exclude_image:
            exclude_images += [exclude_image]

        def decorator(
            action: Union[
                Callable[[Dict[str, Position], np.ndarray], bool],
                Callable[[Dict[str, Position]], bool],
                Callable[[], bool],
            ]
        ):
            """
            装饰器
            :param action: 页面操作函数
            :return:
            """
            logger.debug(f"添加页面：{name}")
            self._pages.append(
                Page(
                    name=name,
                    priority=priority,
                    action=action,
                    targetTexts=target_texts,
                    targetImages=target_images,
                    excludeTexts=exclude_texts,
                    excludeImages=exclude_images,
                    condition=condition,
                    sleep=sleep,
                )
            )

        return decorator

    def conditional(self, name: str, condition: Callable[[], bool]):
        """
        添加一个条件操作任务 装饰器
        :param name: 条件操作名称
        :param condition: 条件函数 返回值为bool lambda表达式
        :return:
        """

        def decorator(action: Callable[[], bool]):
            """
            装饰器
            :param action: 操作函数
            :return:
            """
            if not callable(action):
                raise ValueError("条件操作函数必须为可调用对象")
            logger.debug(f"添加条件操作：{name}")

            self._conditionalActions.append(
                ConditionalAction(name=name, condition=condition, action=action)
            )

        return decorator

    def __call__(self):
        """
        任务匹配
        :return:  bool
        """
        img = screenshot()  # 截图
        ocr_results = self.ocr(img)  # OCR识别
        for page in self._pages:  # 遍历页面
            match_page = page(img, ocr_results)  # 页面匹配
            if match_page:
                state_zero.currentPageName = page.name  # 设置当前页面名称
                logger.debug(
                    f"进入副本次数：{state_zero.fightCount} 当前页面：{page.name}"
                )
                sig = inspect.signature(page.action)  # 获取页面操作函数参数
                params = {}
                for name, param in sig.parameters.items():
                    if param.annotation == Dict[str, Position]:
                        params[name] = page.matchPositions  # 设置匹配位置
                    if param.annotation == np.ndarray:
                        params[name] = img.copy()  # 拷贝图片
                page.action(**params)  # 执行页面操作函数
                if page.sleep:
                    time.sleep(page.sleep)
                self.lastPageName = page.name  # 设置上次页面名称
                break  # 匹配成功后跳出循环

        # 遍历事件操作
        for conditional_action in self._conditionalActions:
            # 如果条件操作函数返回True则执行操作函数
            if conditional_action():
                logger.debug(f"当前条件操作：{conditional_action.name}")
                conditional_action.action()

    def run(self):
        """
        阻塞运行任务
        :return:
        """
        self._pages = sorted(self._pages, key=lambda x: x.priority, reverse=True)
        self._running = True  # 设置运行状态为True
        # self._pause = False
        while self._running:  # 当运行状态为True时循环
            if self._pause:
                logger.info("执行等待")
                time.sleep(1)
                continue
            self()  # 执行任务
        logger.debug("任务循环结束")

    def stop(self):
        """
        停止任务
        :return:
        """
        self._running = False
        logger.debug("等待当前任务循环结束")

    def pause(self):
        """
        暂停任务
        :return:
        """
        logger.info("暂停")
        self._pause = True

    def restart(self):
        """
        重启任务
        :return:
        """
        self._pause = False

    def is_running(self):
        """
        是否运行中:给战斗程序调用，检查是否继续运行,暂停则返回False，否则返回self._running
        """

        if self._pause:
            return False
        return self._running

    def find_text(
        self,
        target: str | Pattern | TextMatch = None,
        targets: List[str | Pattern | TextMatch] = None,
    ) -> Position | None:
        """
        查找文本
        :param target: 目标文本
        :param targets: 目标文本列表
        :return:
        """
        # 如果目标列表为None则转换为列表
        targets = targets or []
        # 将 目标 添加到目标列表
        if target:
            targets += [target]
        # 检查目标类型是否为 TextMatch 如果不是则转换为 TextMatch
        targets = [
            Page.str2_text_match(item) if not isinstance(item, TextMatch) else item
            for item in targets
        ]
        img = screenshot()
        ocr_results = self.ocr(img)
        for item in targets:
            if position := Page.text_match(item, ocr_results):
                return position
        return None

    def wait_text(
        self,
        target: str | Pattern | TextMatch = None,
        targets: List[str | Pattern | TextMatch] = None,
        timeout: float = 10,
    ) -> Position | None:
        """
        等待文本
        :param target: 目标文本
        :param targets: 目标文本列表
        :param timeout: 超时时间
        :return:
        """
        # 如果目标列表为None则转换为列表
        targets = targets or []
        # 将 目标 添加到目标列表
        if target:
            targets += [target]
        # 检查目标类型是否为 TextMatch 如果不是则转换为 TextMatch
        targets = [
            Page.str2_text_match(item) if not isinstance(item, TextMatch) else item
            for item in targets
        ]
        start_time = time.time()
        while time.time() - start_time < timeout:
            if position := self.find_text(targets=targets):
                return position

    @staticmethod
    def find_image(
        target: str | Path | np.ndarray | ImageMatch = None,
        targets: List[str | Path | np.ndarray | ImageMatch] = None,
    ) -> Position | None:
        """
        查找图片
        :param target: 目标图片
        :param targets: 目标图片列表
        :return:
        """
        # 如果目标列表为None则转换为列表
        targets = targets or []
        # 将 目标 添加到目标列表
        if target:
            targets += [target]
        # 检查目标类型是否为 ImageMatch 如果不是则转换为 ImageMatch
        targets = [
            Page.str2_image_match(item) if not isinstance(item, ImageMatch) else item
            for item in targets
        ]
        img = screenshot()
        for item in targets:
            if position := Page.image_match(item, img):
                return position
        return None

    @staticmethod
    def wait_image(
        target: str | Path | np.ndarray | ImageMatch,
        targets: List[str | Path | np.ndarray | ImageMatch] = None,
        timeout: float = 10,
    ) -> Position | None:
        """
        等待图片
        :param target: 目标图片
        :param targets: 目标图片列表
        :param timeout: 超时时间
        :return:
        """
        # 如果目标列表为None则转换为列表
        targets = targets or []
        # 将 目标 添加到目标列表
        if target:
            targets += [target]
        # 检查目标类型是否为 ImageMatch 如果不是则转换为 ImageMatch
        targets = [
            Page.str2_image_match(item) if not isinstance(item, ImageMatch) else item
            for item in targets
        ]
        start_time = time.time()
        while time.time() - start_time < timeout:
            if position := _Task.find_image(targets=targets):
                return position
        return None


# 统一使用paddle_ocr
task_zero = _Task(ocr=paddle_ocr)
task_money = _Task(ocr=paddle_ocr)
task_fight = _Task(ocr=paddle_ocr)
task_code = _Task(ocr=paddle_ocr)
task_daily = _Task(ocr=paddle_ocr)
