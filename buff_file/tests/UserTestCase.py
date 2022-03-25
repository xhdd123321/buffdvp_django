#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 14:54
# @Author  : 10711
# @File    : UserTestCase.py
# @Software: PyCharm
# @Description: UserTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    """
    基于用户测试基类
    """
    def setUp(self):
        self.user_url = 'http://127.0.0.1:8000/user_api/'

        # 普通账号
        self.test_user = {
            'username': 'test_user',
            'password': 'abc123456',
        }
        self.my_admin = self.do_register(**self.test_user)
        # self.my_admin = get_user_model().objects.create_user(**self.test_user)

        # 管理员账号
        self.admin_user = {
            'username': 'admin_user',
            'password': '888888',
        }
        self.my_admin = get_user_model().objects.create_superuser(**self.admin_user)

    def do_login(self, username, password):
        form = {'username': username, 'password': password}
        resp = self.client.post(self.user_url + 'login/', form, format='json')
        return resp

    def do_logout(self):
        resp = self.client.delete(self.user_url + 'logout/', format='json')
        return resp

    def do_register(self, username, password):
        form = {'username': username, 'password': password, 're_password': password}
        resp = self.client.post(self.user_url + 'user/', form, format='json')
        return resp

    def do_users_delete(self, pk):
        resp = self.client.delete(self.user_url + 'user/' + str(pk) + '/', format='json')
        return resp
