# -*- coding: utf-8 -*-
"""
@file: check_update.py
@time: 2024/8/11
@auther: sMythicalBird
"""
import requests
import json
import zipfile
import tempfile
import os
import sys
from pathlib import Path
import shutil


RootPath = Path(__file__).parent.parent.parent

api = "https://api.github.com/repos/sMythicalBird/ZenlessZoneZero-Auto"
web_page = "https://github.com/sMythicalBird/ZenlessZoneZero-Auto"
url = "https://codeload.github.com/sMythicalBird/ZenlessZoneZero-Auto/zip/refs/heads/master"
release_url = "https://github.com/sMythicalBird/ZenlessZoneZero-Auto/releases"


def get_data():
    response = requests.get(url)
    return url, response.content


# 获取版本号和当前更新时间
def get_version():
    # 拉取 API
    all_info = requests.get(api).json()
    # 获得更新时间
    cur_update = all_info["updated_at"]
    # 获得版本信息
    tag_name = requests.get(all_info["tags_url"]).json()[0]["name"]
    version_get = {"tag_name": tag_name, "cur_update": cur_update}
    return version_get


def load_version():
    with open("version.json", "r") as load_f:
        try:
            load_dict = json.load(load_f)
            return load_dict
        except:
            print("本地版本信息错误")


def move_and_overwrite(source_dir, target_dir):
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            else:
                os.remove(target_path)

        shutil.move(source_path, target_path)


def download():
    url, data = get_data()  # data为byte字节

    _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
    _tmp_file.write(data)  # byte字节数据写入临时文件

    zf = zipfile.ZipFile(_tmp_file, mode="r")
    for names in zf.namelist():
        f = zf.extract(names, RootPath.parent)  # 解压到主目录下
    zf.close()
    # 覆盖当前项目文件
    source_dir = RootPath.parent / "ZenlessZoneZero-Auto-master"
    print("move")
    move_and_overwrite(source_dir, RootPath)
    # 删除多余文件
    shutil.rmtree(source_dir)


def check_update():
    cur_version = get_version()
    if not os.path.exists("version.json"):
        with open("version.json", "w") as f:
            json.dump(cur_version, f)
        print("首次运行，已记录版本信息")
    pre_version = load_version()
    if cur_version["tag_name"] != pre_version["tag_name"]:
        print(cur_version["tag_name"] + "版本已发布,请前往" + release_url + "下载")
        return
    if cur_version["cur_update"] != pre_version["cur_update"]:
        print("检测到新版本，正在下载")
        return
    print("当前为最新版本")


if __name__ == "__main__":
    check_update()
    # download()
