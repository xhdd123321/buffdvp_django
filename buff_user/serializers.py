#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/28 13:38
# @Author  : 10711
# @File    : serializers.py
# @Software: PyCharm
# @Description: serializers

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'gender', 'mobile', 'email', 'image', 'user_type', 'is_superuser', 'date_joined')
        read_only_fields = ('username', 'user_type', 'is_superuser', 'date_joined')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'gender', 'mobile', 'email', 'image', 'user_type', 'last_login', 'is_superuser')


class CreateUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 're_password', 'nick_name', 'gender', 'email', 'mobile')
        extra_kwargs = {
            'username': {'min_length': 3, 'max_length': 12},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if not password == re_password:
            raise ValidationError('两次密码不一致')
        attrs.pop('re_password')  # re_password不存数据库，剔除
        return attrs
