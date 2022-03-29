#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/8 21:05
# @Author  : 10711
# @File    : Analyzer.py
# @Software: PyCharm
# @Description: Analyzer
import os
from heapq import heappush, heapreplace
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

    def analysis_describe(self):
        df = self.df
        describe = df.describe()
        index_list = describe.index.values.tolist()
        header_list = ['title'] + index_list

        body_list = []
        describe_dict = describe.to_dict()
        for key in describe_dict.keys():
            describe_dict[key]['title'] = key
            _dict = describe_dict[key]
            body_list.append(_dict)
        res = {
            'header': header_list,
            'body': body_list
        }
        return res

    def analysis_by_count(self):
        df = self.df
        res = list()
        for column in df.columns.tolist():
            if not df[column].is_unique:
                # print(df[column].unique())
                # print(df.groupby(column).size())
                # print(df.groupby(column).size().to_dict())
                res.append((df.groupby(column).size().to_dict(), column))
        return res

    def analysis_by_twocol(self):
        df = self.df
        corr = df.corr()
        row_len = corr.shape[0]
        col_len = corr.shape[1]
        heap = []
        for i in range(0, row_len):
            cur_row = corr.iloc[i]
            for j in range(i + 1, col_len):
                x = cur_row[j]
                if len(heap) < 3:
                    heappush(heap, x)
                else:
                    if heap[0] < x:
                        heapreplace(heap, x)
        index = 0
        header_list = corr.columns.values.tolist()
        res = []
        for i in range(0, row_len):
            cur_row = corr.iloc[i]
            for j in range(i + 1, col_len):
                x = cur_row[j]
                if x in heap:
                    heap.remove(x)
                    _dict = {
                        header_list[i]: df[header_list[i]].to_list(),
                        header_list[j]: df[header_list[j]].to_list()
                    }
                    res.append(_dict)
        return res










