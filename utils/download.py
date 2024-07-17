# -*- coding: utf-8 -*-
"""
@software: PyCharm
@file: download.py
@time: 2024/7/10 上午10:16
@author SuperLazyDog
"""
import sys
import time
from pathlib import Path

import requests
from tqdm import tqdm

from .init import logger, RootPath
from .utils import retry


def download_with_progressbar(url: str, save_path: Path):
    """
    下载文件
    :param url:  下载链接
    :param save_path:  保存路径
    :return:
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise Exception("下载失败！")
        total_size_in_bytes = int(response.headers.get("content-length", 1))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(save_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    except Exception as e:
        logger.exception(e)
        logger.error("下载文件失败！请尝试手动下载！")
        logger.error("下载链接：" + url)
        modelsPath = save_path.parent
        logger.error(f"解压后保存路径：{modelsPath}")
        sys.exit(0)


DownLoadPath = RootPath / "download"
if not DownLoadPath.exists():
    DownLoadPath.mkdir()
# DownLoadBaseUrl = "https://file.caiyun.fun/download/zzz/"
DownLoadBaseUrl = "https://zzz.caiyun.fun/"
FileListUrl = DownLoadBaseUrl + "filelist.txt"


@retry(3)
def check_file():
    """
    检查文件列表中的文件是否存在，不存在则下载
    :return:
    """
    logger.debug("开始检查文件！")
    file_list = requests.get(FileListUrl).text.split("\n")
    for file in file_list:
        file = file.strip()
        file_path = DownLoadPath / file
        need_download = False
        if file_path.exists():
            # 获取文件最后修改时间
            file_time = file_path.stat().st_mtime
            # 获取网络文件最后修改时间
            response = requests.head(DownLoadBaseUrl + file)
            last_modified = response.headers.get("Last-Modified", None)
            if not last_modified:
                raise Exception("获取文件最后修改时间失败！")
            last_modified = (
                last_modified.strip() + "+00:00"
                if last_modified.strip().endswith("GMT")
                else last_modified.strip()
            )
            # 转换时间格式
            last_modified = time.strptime(last_modified, "%a, %d %b %Y %H:%M:%S %Z%z")
            # 转换为时间戳
            last_modified = time.mktime(last_modified)
            # 判断是否需要下载
            if last_modified > file_time:
                need_download = True
                logger.info(f"文件：{file} 需要更新！")
        else:
            need_download = True
        if need_download:
            download_with_progressbar(DownLoadBaseUrl + file, file_path)
            logger.info(f"下载文件：{file}")

    logger.debug("文件检查完成！")


check_file()
