# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: schema.py
@time: 2024/6/25 下午12:07
@author SuperLazyDog
"""
from re import Pattern, template

from pydantic import BaseModel, Field, model_validator


class Position(BaseModel):
    x1: int = Field(None, title="x1")
    y1: int = Field(None, title="y1")
    x2: int = Field(None, title="x2")
    y2: int = Field(None, title="y2")

    @property
    def x(self):
        return (self.x1 + self.x2) / 2

    @property
    def y(self):
        return (self.y1 + self.y2) / 2

    @property
    def w(self):
        return self.x2 - self.x1

    @property
    def h(self):
        return self.y2 - self.y1

    @model_validator(mode="before")
    def check_coordinates(cls, values):
        x1, y1, x2, y2 = (
            values.get("x1"),
            values.get("y1"),
            values.get("x2"),
            values.get("y2"),
        )
        if any(v is None for v in [x1, y1, x2, y2]):
            raise ValueError("All coordinates must be provided")
        return values

    def __call__(self):
        return self.x1, self.y1, self.x2, self.y2

    def __str__(self):
        return f"({self.x1}, {self.y1}, {self.x2}, {self.y2})"

    def __repr__(self):
        return f"({self.x1}, {self.y1}, {self.x2}, {self.y2})"

    # 实现 subscriptable
    def __getitem__(self, item):
        if item == 0:
            return self.x1
        elif item == 1:
            return self.y1
        elif item == 2:
            return self.x2
        elif item == 3:
            return self.y2
        else:
            raise IndexError("Index out of range")

    def __contains__(self, item):
        if (
            item.x1 >= self.x1
            and item.y1 >= self.y1
            and item.x2 <= self.x2
            and item.y2 <= self.y2
        ):
            return True
        else:
            return False

    def contain(self, item):
        return item in self


class ImgPosition(Position):
    confidence: float = Field(0, title="识别置信度")

    def __str__(self):
        return f"({self.x1}, {self.y1}, {self.x2}, {self.y2}, {self.confidence})"

    def __repr__(self):
        return f"({self.x1}, {self.y1}, {self.x2}, {self.y2}, {self.confidence})"


class OcrResult(BaseModel):
    text: str = Field(title="识别结果")
    position: Position = Field(title="识别位置")
    confidence: float = Field(0, title="识别置信度")


class OcrWordResult(OcrResult):
    word_positions: list[Position] = Field(title="识别单词位置")

    def words_position(self, words: str | Pattern) -> Position | None:
        """
        获取单词的位置
        :param words: 词
        :return:
        """
        if isinstance(words, str):
            words = template(words)
        matchInfo = words.search(self.text)
        if not matchInfo:
            return None
        startWord = self.word_positions[matchInfo.start()]
        endWord = self.word_positions[matchInfo.end() - 1]
        return Position(x1=startWord.x1, y1=startWord.y1, x2=endWord.x2, y2=endWord.y2)
