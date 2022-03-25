#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 1:36
# @Author  : 10711
# @File    : Extractor.py
# @Software: PyCharm
# @Description: Extractor
from pandas import DataFrame

from buff_file.models import File


class Extractor:
    def __init__(self, file: File):
        self.file = file
        self.res = None
        self.title = ""
        self.header = None
        self.body = None
        self.df = None
        self.read_file()

    def read_file(self):
        """
        读取文件
        :return:
        """

    def title_handle(self):
        """
        数据处理
        :return:
        """

    def header_handle(self):
        """
        数据处理
        :return:
        """

    def body_handle(self):
        """
        数据处理
        :return:
        """

    def get_title(self):
        """
        获取标题
        :return:
        """
        self.title_handle()
        return self.title

    def get_header(self):
        """
        获取表头
        :return:
        """
        self.header_handle()
        return self.header

    def get_body(self):
        """
        获取表体
        :return:
        """
        self.body_handle()
        return self.body
