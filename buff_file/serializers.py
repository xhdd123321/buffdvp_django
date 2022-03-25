#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 23:24
# @Author  : 10711
# @File    : serializers.py
# @Software: PyCharm
# @Description: serializers
from rest_framework import serializers

from utils.path_utils import get_filepath_filename_extension
from .models import File


class FileSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = File
        fields = ('id', 'name', 'type', 'file', 'create_time', 'user')


class FileCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'type', 'file', 'create_time')
        read_only_fields = ('id', 'name', 'type', 'create_time')

    def create(self, validated_data):
        file = File.objects.create(**validated_data)
        file_url = file.file.name
        filepath, basename, extension = get_filepath_filename_extension(file_url)
        file.name = basename
        file.type = extension
        file.save()
        return file
