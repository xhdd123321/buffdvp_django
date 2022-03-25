#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/1 21:10
# @Author  : 10711
# @File    : Enums.py
# @Software: PyCharm
# @Description: Enums
from enum import Enum, unique


@unique
class RespMsgEnum(Enum):
    fail = 0
    success = 1
