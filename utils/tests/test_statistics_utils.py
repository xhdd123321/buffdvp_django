#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/22 21:06
# @Author  : 10711
# @File    : test_statistics_utils.py
# @Software: PyCharm
import os
import platform

from rest_framework.test import APITestCase
from utils.statistics_utils import get_cpu_info, get_net_info, get_mem_info


class TestStatisticsUtils(APITestCase):
    def test_get_cpu_info(self):
        res = get_cpu_info()
        print(res)

    def test_get_net_info(self):
        res = get_net_info()

        print(platform.platform())
        print(res)

    def test_mem_info(self):
        res = get_mem_info()
        print(res)
