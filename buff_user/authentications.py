#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/18 17:08
# @Author  : 10711
# @File    : authentications.py
# @Software: PyCharm
# @Description: authentications
from rest_framework.authentication import SessionAuthentication


class MySessionAuthentication(SessionAuthentication):

    def authenticate_header(self, request):
        return 'Session: Authentication credentials were not provided.'
