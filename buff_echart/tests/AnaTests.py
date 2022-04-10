#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/4/10 16:45
# @Author  : 10711
# @File    : AnaTests.py
# @Software: PyCharm
# @Description: AnaTests
import csv
import os
import time

from rest_framework import status
from rest_framework.test import URLPatternsTestCase, APITestCase
from django.urls import path, include


class AnaTests(APITestCase, URLPatternsTestCase):
    fixtures = ['testDB.json']

    urlpatterns = [
        path('echart_api/', include('buff_echart.urls')),
        path('user_api/', include('buff_user.urls')),
    ]

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/echart_api/'
        self.user_url = 'http://127.0.0.1:8000/user_api/'

    def tearDown(self) -> None:
        pass

    def do_login_admin(self):
        form = {'username': 'admin', 'password': '123456'}
        resp = self.client.post(self.user_url + 'login/', form, format='json')
        return resp

    def do_ana_compare(self, chart_id):
        form = {'chart_id': chart_id}
        resp = self.client.post(self.base_url + 'ana/compare/', form, format='json')
        return resp

    def do_ehcart_create(self, chart_id):
        form = {'chart_id': chart_id}
        resp = self.client.post(self.base_url + 'echart/', form, format='json')
        return resp

    def test_cache_ehcart_create(self):
        echart_id = 41
        pwd = os.path.dirname(__file__)
        testData = os.path.join(pwd, 'ehcartCreate_testData.csv')
        resp = self.do_ehcart_create(echart_id)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.do_login_admin()

        for i in range(0, 50):
            time.sleep(5)

            start_time = time.time()
            resp = self.do_ehcart_create(echart_id)
            end_time = time.time()
            no_cache_time = round((end_time - start_time) * 1000, 2)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertFalse(resp.data.get('cache'))

            time.sleep(5)

            start_time = time.time()
            resp = self.do_ehcart_create(echart_id)
            end_time = time.time()
            cache_time = round((end_time - start_time) * 1000, 2)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertTrue(resp.data.get('cache'))

            if no_cache_time < cache_time:
                continue

            with open(testData, "r+", newline='') as f:
                reader = csv.reader(f)
                count = 0
                for row in reader:
                    count += 1
                writer = csv.writer(f, delimiter=',')
                if count == 0:
                    writer.writerow(['id', 'no_cache_time', 'cache_time'])
                    count += 1
                writer.writerow([count, no_cache_time, cache_time])

    def test_cache_ana_compare(self):
        echart_id = 41
        pwd = os.path.dirname(__file__)
        testData = os.path.join(pwd, 'anaCompare_testData.csv')
        resp = self.do_ana_compare(echart_id)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.do_login_admin()

        for i in range(0, 50):
            time.sleep(5)

            start_time = time.time()
            resp = self.do_ana_compare(echart_id)
            end_time = time.time()
            no_cache_time = round((end_time - start_time) * 1000, 2)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertFalse(resp.data.get('cache'))

            time.sleep(5)

            start_time = time.time()
            resp = self.do_ana_compare(echart_id)
            end_time = time.time()
            cache_time = round((end_time - start_time) * 1000, 2)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertTrue(resp.data.get('cache'))

            if no_cache_time < cache_time:
                continue

            with open(testData, "r+", newline='') as f:
                reader = csv.reader(f)
                count = 0
                for row in reader:
                    count += 1
                writer = csv.writer(f, delimiter=',')
                if count == 0:
                    writer.writerow(['id', 'no_cache_time', 'cache_time'])
                    count += 1
                writer.writerow([count, no_cache_time, cache_time])
