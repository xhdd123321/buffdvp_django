#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/8 18:03
# @Author  : 10711
# @File    : serializers.py
# @Software: PyCharm
# @Description: serializers
from rest_framework import serializers


class EchartSerializer(serializers.Serializer):
    chart_id = serializers.IntegerField(required=True)

