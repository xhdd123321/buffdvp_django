#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/8 21:05
# @Author  : 10711
# @File    : Analyzer.py
# @Software: PyCharm
# @Description: Analyzer
import os
from io import BytesIO

import pandas as pd
from pandas import DataFrame

from buff_data.models import Chart
from buffdvp_django.settings import MEDIA_ROOT


class Analyzer:
    def __init__(self, chart: Chart):
        self.chart = chart
        self.df = DataFrame()

        self.convert_to_dataframe()

    def convert_to_dataframe(self):
        body = self.chart.body
        header = self.chart.header
        self.df = pd.DataFrame(body, columns=header)
        print(self.df)

    def export_to_excel(self):
        path = os.path.join(MEDIA_ROOT, 'export', self.chart.title + '.xlsx')
        self.df.to_excel(path, index=False)
        return path

    def export_to_csv(self):
        path = os.path.join(MEDIA_ROOT, 'export', self.chart.title + '.csv')
        self.df.to_csv(path, index=False)
        return path

    def analysis_by_count(self):
        df = self.df
        res = list()
        for column in df.columns.tolist():
            if not df[column].is_unique:
                print(df[column].unique())
                print(df.groupby(column).size())
                print(df.groupby(column).size().to_dict())
                res.append((df.groupby(column).size().to_dict(), column))
        return res

    def analysis_by_twocol(self):
        df = self.df
        print(df.dtypes)






