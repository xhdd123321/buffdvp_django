#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/1 15:52
# @Author  : 10711
# @File    : RedisTests.py
# @Software: PyCharm
# @Description: RedisTests

from django.core.cache import cache
from rest_framework.test import APITestCase


class RedisTests(APITestCase):
    def setUp(self):
        self.test_key = 'foo'
        self.test_value = 'bar'

    def test_redis_get_delete(self):
        t_key = self.test_key
        t_value = self.test_value
        cache.set(t_key, t_value)
        self.assertEqual(cache.get(t_key), t_value)
        self.assertTrue(cache.delete(t_key))
        self.assertIsNone(cache.get(t_value))

