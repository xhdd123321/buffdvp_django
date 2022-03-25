#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/28 13:29
# @Author  : 10711
# @File    : urls.py
# @Software: PyCharm
# @Description: urls
from django.conf import settings
from rest_framework import routers
from django.urls import include, path

from buff_file.views import FileModelViewSet

router = routers.DefaultRouter()
router.register(r'file', FileModelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
