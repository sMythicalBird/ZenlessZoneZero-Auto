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


def download():
    url, data = get_data()  # data为byte字节

    _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
    _tmp_file.write(data)  # byte字节数据写入临时文件

    with zipfile.ZipFile(_tmp_file, mode="r") as zf:
        for member in zf.infolist():
            # 替换最外层目录
            extracted_path = RootPath.name / Path(*Path(member.filename).parts[1:])
            target_path = RootPath.parent / extracted_path
            if member.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)


version_path = Path(__file__).parent / "version.json"


def load_version():
    with open(version_path, "r") as load_f:
        try:
            load_dict = json.load(load_f)
            return load_dict
        except:
            print("本地版本信息错误")


def check_update():
    cur_version = get_version()
    if not version_path.exists():
        with open(version_path, "w") as f:
            json.dump(cur_version, f)
    pre_version = load_version()
    if ".".join(cur_version["tag_name"].split(".")[:2]) != ".".join(
        pre_version["tag_name"].split(".")[:2]
    ):
        return 0, cur_version["tag_name"] + "版本已发布,请前往" + release_url + "下载"
    if cur_version["cur_update"] != pre_version["cur_update"]:
        with open(version_path, "w") as f:
            json.dump(cur_version, f)
        return 1, "检测到新版本，正在下载"
    return 0, "当前为最新版本"


def release_version():
    cur_version = get_version()
    cur_version["tag_name"] = "v2.4.0"
    with open(version_path, "w") as f:
        json.dump(cur_version, f)


if __name__ == "__main__":
    check_update()  # 打包时生成一份版本文档
    # download()
    # release_version()
