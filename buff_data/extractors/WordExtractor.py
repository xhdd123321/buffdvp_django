#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 1:28
# @Author  : 10711
# @File    : WordExtractor.py
# @Software: PyCharm
# @Description: WordExtractor
from rest_framework.exceptions import ParseError

from buff_file.models import File
from .Extractor import Extractor


class WordExtractor(Extractor):
    def __init__(self, file: File):
        super().__init__(file)
        raise ParseError("无法提取该类型文件")
