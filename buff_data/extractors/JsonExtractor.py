#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/4/10 23:45
# @Author  : 10711
# @File    : JsonExtractor.py
# @Software: PyCharm
# @Description: JsonExtractor
import pandas as pd
from pandas import DataFrame

from buff_data.extractors.Extractor import Extractor
from buff_file.models import File


class JsonExtractor(Extractor):
    def __init__(self, file: File):
        super().__init__(file)

    def read_file(self):
        self.df = pd.read_json(self.file.file)

    def title_handle(self):
        self.title = self.file.name

    def header_handle(self):
        df = self.df
        self.header = df.columns.tolist()

    def body_handle(self):
        df: DataFrame = self.df
        self.body = df.values.tolist()
