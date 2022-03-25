#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 14:46
# @Author  : 10711
# @File    : FileTests.py
# @Software: PyCharm
# @Description: FileTests
import os
import shutil

from django.conf import settings
from rest_framework import status
from rest_framework.test import URLPatternsTestCase
from django.urls import path, include
from ..apps import BuffFileConfig as BuffConfig

from buff_file.tests.UserTestCase import UserTestCase


class FileTests(UserTestCase, URLPatternsTestCase):
    urlpatterns = [
        path('file_api/', include('buff_file.urls')),
        path('user_api/', include('buff_user.urls')),
    ]

    def setUp(self):
        super().setUp()
        self.base_url = 'http://127.0.0.1:8000/file_api/'
        pwd = os.path.dirname(__file__)
        self.test_file_name = 'test_file.xlsx'
        self.test_file_path = os.path.join(pwd, 'source', self.test_file_name)

    def tearDown(self) -> None:
        # 结束时删除测试用户资源文件夹
        admin_file_dir = os.path.join(settings.MEDIA_ROOT,
                                      os.path.dirname(BuffConfig.re_file(self.admin_user.get('username'), self.test_file_name)))
        user_file_dir = os.path.join(settings.MEDIA_ROOT,
                                     os.path.dirname(BuffConfig.re_file(self.test_user.get('username'), self.test_file_name)))
        if os.path.isdir(admin_file_dir):
            shutil.rmtree(admin_file_dir)
            print(self.admin_user.get('username') + "文件夹已删除")
        if os.path.isdir(user_file_dir):
            shutil.rmtree(user_file_dir)
            print(self.test_user.get('username') + "文件夹已删除")

    def do_file_create(self, file_path):
        with open(file_path, 'rb') as fp:
            form = {'file': fp}
            resp = self.client.post(self.base_url + 'file/', form, format='multipart')
        return resp

    def do_file_delete(self, pk):
        resp = self.client.delete(self.base_url + 'file/' + str(pk) + '/', format='json')
        return resp

    def do_file_retrieve(self, pk):
        resp = self.client.get(self.base_url + 'file/' + str(pk) + '/', format='json')
        return resp

    def do_file_list(self):
        resp = self.client.get(self.base_url + 'file/', format='json')
        return resp

    def test_file_create(self):
        # 未登录 创建文件
        resp = self.do_file_create(self.test_file_path)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 登录普通用户 创建文件
        resp = self.do_login(**self.test_user)
        username = resp.data.get('data').get('username')
        resp = self.do_file_create(self.test_file_path)
        pk = resp.data.get('id')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # 检测文件是否创建
        upload_to_path = BuffConfig.re_file(username, self.test_file_name)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, upload_to_path)))
        # 登录管理员用户 创建文件
        self.do_login(**self.admin_user)
        resp = self.do_file_create(self.test_file_path)
        pk = resp.data.get('id')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_file_delete(self):
        # 登录普通用户 创建文件
        resp = self.do_login(**self.test_user)
        username = resp.data.get('data').get('username')
        resp = self.do_file_create(self.test_file_path)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        pk = resp.data.get('id')
        # 删除文件
        resp = self.do_file_delete(pk)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # 检测文件是否已删除
        upload_to_path = BuffConfig.re_file(username, self.test_file_name)
        self.assertFalse(os.path.exists(os.path.join(settings.MEDIA_ROOT, upload_to_path)))

    def test_file_retrieve(self):
        # 登录普通用户
        self.do_login(**self.test_user)
        # 创建文件 file1
        resp = self.do_file_create(self.test_file_path)
        pk = resp.data.get('id')
        # 查文件 file1
        resp = self.do_file_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 登录管理员
        self.do_login(**self.admin_user)
        # 查文件 file1
        resp = self.do_file_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 创建文件 file2
        resp = self.do_file_create(self.test_file_path)
        pk = resp.data.get('id')
        # 查文件 file2
        resp = self.do_file_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 登录普通用户
        self.do_login(**self.test_user)
        # 查文件 file2
        resp = self.do_file_retrieve(pk)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_file_list(self):
        # 未登录 查找文件
        resp = self.do_file_list()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # 普通用户 创建文件 查列表
        self.do_login(**self.test_user)
        self.do_file_create(self.test_file_path)
        resp = self.do_file_list()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('count'), 1)
        # 管理员 创建文件 查列表
        self.do_login(**self.admin_user)
        self.do_file_create(self.test_file_path)
        resp = self.do_file_list()
        self.assertEqual(resp.data.get('count'), 2)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 普通用户 查列表
        self.do_login(**self.test_user)
        resp = self.do_file_list()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('count'), 1)

    def test_file_update(self):
        """
        更新接口不存在
        """
        self.do_login(**self.admin_user)
        resp = self.client.put(self.base_url + 'file/1/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

