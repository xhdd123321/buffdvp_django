#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 1:26
# @Author  : 10711
# @File    : ExcelExtractor.py
# @Software: PyCharm
# @Description: ExcelExtractor
import pandas as pd
from pandas import DataFrame

from buff_file.models import File
from .Extractor import Extractor


class ExcelExtractor(Extractor):
    def __init__(self, file: File):
        super().__init__(file)

    def read_file(self):
        self.df = pd.read_excel(self.file.file)

    def title_handle(self):
        self.title = self.file.name

    def header_handle(self):
        df = self.df
        self.header = df.columns.tolist()

    def body_handle(self):
        df: DataFrame = self.df
        self.body = df.values.tolist()
