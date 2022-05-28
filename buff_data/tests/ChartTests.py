#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/5/9 19:03
# @Author  : 10711
# @File    : ChartTests.py
# @Software: PyCharm
# @Description: ChartTests
from rest_framework import status
from rest_framework.test import URLPatternsTestCase, APITestCase
from django.urls import path, include


class CharTests(APITestCase, URLPatternsTestCase):
    fixtures = ['testDB.json']

    urlpatterns = [
        path('data_api/', include('buff_data.urls')),
        path('user_api/', include('buff_user.urls')),
    ]

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/data_api/'
        self.user_url = 'http://127.0.0.1:8000/user_api/'

        self.chart_form = {
            'file_id': 12
        }

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

    def do_login_other(self):
        form = {'username': 'test001', 'password': 'test001'}
        resp = self.client.post(self.user_url + 'login/', form, format='json')
        return resp

    def do_logout(self):
        resp = self.client.delete(self.user_url + 'logout/', format='json')
        return resp

    def do_chart_create(self, form):
        resp = self.client.post(self.base_url + 'chart/', form, format='json')
        return resp

    def do_chart_delete(self, pk):
        resp = self.client.delete(self.base_url + 'chart/' + str(pk) + '/', format='json')
        return resp

    def do_chart_update(self, pk, form):
        resp = self.client.put(self.base_url + 'chart/' + str(pk) + '/', form, format='json')
        return resp

    def do_chart_retrieve(self, pk):
        resp = self.client.get(self.base_url + 'chart/' + str(pk) + '/', format='json')
        return resp

    def do_chart_list(self):
        resp = self.client.get(self.base_url + 'chart/', format='json')
        return resp

    def test_chart_create(self):
        # 登录前
        resp = self.do_chart_create(self.chart_form)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录普通账号
        self.do_login_user()
        resp = self.do_chart_create(self.chart_form)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.do_logout()
        # 登录管理员账号
        self.do_login_admin()
        resp = self.do_chart_create(self.chart_form)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_chart_delete(self):
        self.do_login_user()
        resp = self.do_chart_create(self.chart_form)
        pk = resp.data.get('id')
        self.do_logout()
        # 登录前
        resp = self.do_chart_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录其他账号
        self.do_login_other()
        resp = self.do_chart_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.do_logout()
        # 登录当前账号
        self.do_login_user()
        resp = self.do_chart_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.do_chart_create(self.chart_form)
        pk = resp.data.get('id')
        self.do_logout()
        # 登录管理员账号
        self.do_login_admin()
        resp = self.do_chart_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_chart_update(self):
        self.do_login_user()
        resp = self.do_chart_create(self.chart_form)
        pk = resp.data.get('id')
        self.do_logout()
        update_form = {'title': 'new_title'}
        # 登录前
        resp = self.do_chart_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录当前账号
        self.do_login_user()
        resp = self.do_chart_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.do_logout()
        # 登录其他账号
        self.do_login_other()
        resp = self.do_chart_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.do_logout()
        # 登录管理员账号
        self.do_login_admin()
        resp = self.do_chart_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_chart_retrieve(self):
        self.do_login_user()
        resp = self.do_chart_create(self.chart_form)
        pk = resp.data.get('id')
        self.do_logout()
        # 登录前
        resp = self.do_chart_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录当前账号
        self.do_login_user()
        resp = self.do_chart_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.do_logout()
        # 登录其他账号
        self.do_login_other()
        resp = self.do_chart_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.do_logout()
        # 登录管理员账号
        self.do_login_admin()
        resp = self.do_chart_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


