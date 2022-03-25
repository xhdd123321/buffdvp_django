#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/1 22:31
# @Author  : 10711
# @File    : UserTests.py
# @Software: PyCharm
# @Description: UserTests
import os
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import path, include
from rest_framework import status

from buff_user.models import Gender
from rest_framework.test import APITestCase, APIClient, URLPatternsTestCase

from ..apps import BuffUserConfig as BuffConfig


class UserTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('user_api/', include('buff_user.urls')),
    ]

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=False)
        self.base_url = 'http://127.0.0.1:8000/user_api/'

        self.register_form = {
            'username': 'local_test',
            'password': '123456789',
            're_password': '123456789',
            'nick_name': 'Nate',
            'gender': Gender.MALE.value,
            'email': '1254878@qq.com',
            'mobile': '18813129781',
        }

        self.login_form = {
            'username': 'local_test',
            'password': '123456789',
        }

        # 注册普通账号
        self.test_user = {
            'username': 'test_user',
            'password': 'abc123456',
            're_password': 'abc123456',
            'nick_name': 'God',
        }
        self.do_register(self.test_user)

        # 注册管理员账号
        self.admin_user = {
            'username': 'admin',
            'password': '888888',
            'email': 'admin@test.com',
        }
        self.my_admin = get_user_model().objects.create_superuser(**self.admin_user)

    def do_login(self, form):
        resp = self.client.post(self.base_url + 'login/', form, format='json')
        return resp

    def do_logout(self):
        resp = self.client.delete(self.base_url + 'logout/', format='json')
        return resp

    def do_register(self, form):
        resp = self.client.post(self.base_url + 'user/', form, format='json')
        return resp

    def do_users_delete(self, pk):
        resp = self.client.delete(self.base_url + 'user/' + str(pk) + '/', format='json')
        return resp

    def do_users_update(self, pk, form):
        resp = self.client.put(self.base_url + 'user/' + str(pk) + '/', form, format='multipart')
        return resp

    def do_users_retrieve(self, pk):
        resp = self.client.get(self.base_url + 'user/' + str(pk) + '/', format='json')
        return resp

    def do_users_list(self):
        resp = self.client.get(self.base_url + 'user/', format='json')
        return resp

    def test_login(self):
        resp = self.do_login(self.login_form)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 限流测试
        # resp = self.do_login(self.login_form)
        # self.assertEqual(resp.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.do_register(self.register_form)
        time.sleep(1)
        resp = self.do_login(self.login_form)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.do_register(self.register_form)
        # 登录前
        resp = self.do_logout()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 登录当前账号
        self.do_login(self.login_form)
        resp = self.do_logout()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 退出登录后
        resp = self.do_logout()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_register(self):
        resp = self.do_register(self.register_form)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # 重复注册
        resp = self.do_register(self.register_form)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete(self):
        resp = self.do_register(self.register_form)
        pk = resp.data.get('id')
        # 登录前
        resp = self.do_users_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录其他账号
        self.do_login(self.test_user)
        resp = self.do_users_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        # 登录当前账号
        self.do_login(self.login_form)
        resp = self.do_users_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # 登录管理员账号
        resp = self.do_register(self.register_form)
        pk = resp.data.get('id')
        self.do_login(self.admin_user)
        resp = self.do_users_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_update(self):
        update_form = {
            'nick_name': 'Mike',
        }
        resp = self.do_register(self.register_form)
        pk = resp.data.get('id')
        # 登录前
        resp = self.do_users_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录其他账号
        self.do_login(self.test_user)
        resp = self.do_users_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        # 登录当前账号
        self.do_login(self.login_form)
        resp = self.do_users_retrieve(pk)
        old_data = resp.data
        old_data['nick_name'] = 'Mike'
        resp = self.do_users_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_data = resp.data
        self.assertEqual(old_data, new_data)
        # 登录管理员账号
        self.do_login(self.admin_user)
        resp = self.do_users_update(pk, update_form)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        resp = self.do_register(self.register_form)
        pk = resp.data.get('id')
        # 登录前
        resp = self.do_users_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录其他账号
        self.do_login(self.test_user)
        resp = self.do_users_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        # 登录当前账号
        self.do_login(self.login_form)
        resp = self.do_users_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 退出登录
        self.do_logout()
        resp = self.do_users_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录管理员账号
        self.do_login(self.admin_user)
        resp = self.do_users_list()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_user_list(self):
        self.do_register(self.register_form)
        # 登录前
        resp = self.do_users_list()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录普通账号
        self.do_login(self.login_form)
        resp = self.do_users_list()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        # 登录管理员账号
        self.do_login(self.admin_user)
        resp = self.do_users_list()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_user_avatar_upload(self):
        # 登录普通账号
        resp = self.do_login(self.test_user)
        pk = resp.data.get('data').get('id')
        username = resp.data.get('data').get('username')
        # 检查头像图片是否为None
        resp = self.do_users_retrieve(pk)
        self.assertIsNone(resp.data.get('image'))
        # 上传头像图片
        pwd = os.path.dirname(__file__)
        test_filename = os.path.join(pwd, 'source', 'test_avatar.jpg')
        with open(test_filename, 'rb') as fp:
            resp = self.do_users_update(pk, {'image': fp})
        filepath = resp.data.get('image')
        upload_to_path = BuffConfig.re_user_avatar(username)
        self.assertEqual(os.path.basename(filepath), os.path.basename(upload_to_path))
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, upload_to_path)))
        # 删除账号同时删除图片
        self.do_users_delete(pk)
        self.assertFalse(os.path.exists(os.path.join(settings.MEDIA_ROOT, upload_to_path)))








