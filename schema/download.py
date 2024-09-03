# -*- coding: utf-8 -*-
"""
@file:      download
@time:      2024/9/3 14:00
@author:    sMythicalBird
"""
import sys
from loguru import logger

import requests
from tqdm import tqdm
from hashlib import md5
from pathlib import Path

RootPath = Path(__file__).parent.parent


def download_with_progressbar(url: str, save_path: Path):
    """
    下载文件
    :param url:  下载链接
    :param save_path:  保存路径
    :return:
    """
    logger.debug(f"下载链接：{url}, 保存路径：{save_path}")
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
    except:
        logger.error("下载文件失败！可尝试手动下载！")
        logger.error("下载链接：" + url)
        modelsPath = save_path.parent
        logger.error(f"解压后保存路径：{modelsPath}")
        if save_path.exists():
            save_path.unlink()
        raise Exception("下载文件失败！")


DownLoadPath = RootPath / "download"
if not DownLoadPath.exists():
    DownLoadPath.mkdir()
DownLoadBaseUrl = [
    "https://alist.caiyun.fun/d/download/zzz/",
    "https://zzz.caiyun.fun/",
    "https://download.caiyun.fun/",
    "http://pan.caiyun.fun/1655577/zzz/",
]


def check_file(retry_count=0):
    """
    检查文件列表中的文件是否存在，不存在则下载
    """
    index = (retry_count // 2) % len(DownLoadBaseUrl)
    fileListUrl = DownLoadBaseUrl[index] + "filelist.json"
    file_list = requests.get(fileListUrl, timeout=3).json()
    for item in file_list:
        file = item["name"].strip()
        file_md5 = item["md5"].strip()
        file_path = DownLoadPath / file
        need_download = False
        # 文件不存在或者文件md5不一致
        if (
            not file_path.exists()
            or md5(file_path.read_bytes()).hexdigest() != file_md5
        ):
            file_path.unlink(missing_ok=True)
            need_download = True
        if need_download:
            logger.info(f"下载文件：{file}")
            download_with_progressbar(
                f"{DownLoadBaseUrl[index]}{file}",
                file_path,
            )
    logger.debug("文件检查完成！")


def check_file_task():
    """
    检查文件列表中的文件是否存在，不存在则下载
    :return:
    """
    retry_count = 0
    check_success = False
    for i in range(8):
        try:
            logger.debug("开始检查文件！")
            check_file(retry_count)
            check_success = True
            break
        except Exception as e:
            logger.error("检查文件失败！" + str(e))
            retry_count += 1
            continue
    if not check_success:
        logger.error("检查文件失败！请检查网络连接后重新启动！")
        sys.exit(1)
