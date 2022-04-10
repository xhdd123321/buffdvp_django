#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 1:29
# @Author  : 10711
# @File    : ExtractorController.py
# @Software: PyCharm
# @Description: ExtractorController
from rest_framework.exceptions import ParseError

from .CsvExtractor import CsvExtractor
from .ExcelExtractor import ExcelExtractor
from buff_file.models import File
from .Extractor import Extractor
from .JsonExtractor import JsonExtractor
from .WordExtractor import WordExtractor


class ExtractorController:
    @staticmethod
    def get_file_extractor(file: File) -> Extractor:
        file_type = file.type
        if file_type in ('.xlsx', '.xls'):
            ext = ExcelExtractor(file)
        elif file_type in ('.docx',):
            ext = WordExtractor(file)
        elif file_type in ('.csv', '.txt'):
            ext = CsvExtractor(file)
        elif file_type in ('.json',):
            ext = JsonExtractor(file)
        else:
            raise ParseError("无法提取该类型文件")
        return ext
