#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/1 20:25
# @Author  : 10711
# @File    : MyResponse.py
# @Software: PyCharm
# @Description: MyResponse
from rest_framework.response import Response


class MyResponse(Response):
    def __init__(self, code=1, msg='ok', data='', status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        dic = {'code': code, 'msg': msg, 'data': data}
        if kwargs:
            dic.update(kwargs)

        super().__init__(data=dic, status=status,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)
