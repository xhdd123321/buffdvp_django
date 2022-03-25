#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/6 0:59
# @Author  : 10711
# @File    : serializers.py
# @Software: PyCharm
# @Description: serializers
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ParseError

from buff_data.extractors import ExtractorController
from buff_data.models import Chart
from buff_file.models import File


class ChartSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Chart
        fields = ('id', 'title', 'header', 'body', 'create_time', 'user')


class ChartListSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Chart
        fields = ('id', 'title', 'create_time', 'user')


class ChartCreateSerializers(serializers.ModelSerializer):
    file_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Chart
        fields = ('id', 'title', 'header', 'body', 'create_time', 'file_id')
        read_only_fields = ('id', 'title', 'header', 'body', 'create_time')

    def create(self, validated_data):
        file_id = validated_data.pop('file_id')
        try:
            file_obj = File.objects.get(id=file_id)
        except File.DoesNotExist:
            raise NotFound("待解析文件不存在")
        extractor = ExtractorController.get_file_extractor(file_obj)
        validated_data['title'] = extractor.get_title()
        validated_data['header'] = extractor.get_header()
        validated_data['body'] = extractor.get_body()
        try:
            chart = Chart.objects.create(**validated_data)
        except TypeError:
            raise ParseError("文件解析失败")
        return chart
