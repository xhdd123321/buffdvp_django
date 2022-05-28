#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/5/9 19:04
# @Author  : 10711
# @File    : DashboardTests.py
# @Software: PyCharm
# @Description: DashboardTests
from rest_framework import status
from rest_framework.test import URLPatternsTestCase, APITestCase
from django.urls import path, include


class DashboardTests(APITestCase, URLPatternsTestCase):
    fixtures = ['testDB.json']

    urlpatterns = [
        path('data_api/', include('buff_data.urls')),
        path('user_api/', include('buff_user.urls')),
    ]

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/data_api/'
        self.user_url = 'http://127.0.0.1:8000/user_api/'

    def tearDown(self) -> None:
        pass

    def do_login_admin(self):
        form = {'username': 'admin', 'password': '123456'}
        resp = self.client.post(self.user_url + 'login/', form, format='json')
        return resp

    def do_login_user(self):
        form = {'username': 'xhdd123321', 'password': 'xhds123321'}
        resp = self.client.post(self.user_url + 'login/', form, format='json')
        return resp

    def do_dashboard_get(self):
        resp = self.client.get(self.base_url + 'dashboard/', format='json')
        return resp

    def test_dashboard_get(self):
        # 未登录
        resp = self.do_dashboard_get()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录普通用户
        self.do_login_user()
        resp = self.do_dashboard_get()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 登录管理员用户
        self.do_login_admin()
        resp = self.do_dashboard_get()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
