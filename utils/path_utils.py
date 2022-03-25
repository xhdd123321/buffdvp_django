#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 20:06
# @Author  : 10711
# @File    : path_utils.py
# @Software: PyCharm
# @Description: path_utils
import os


def get_filepath_filename_extension(fileUrl):
    """
    由文件绝对路径提取文件名
    :param fileUrl:
    :return:
    """
    filepath, filename = os.path.split(fileUrl)
    filename, extension = os.path.splitext(filename)
    return filepath, filename, extension
