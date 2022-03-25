#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/28 13:29
# @Author  : 10711
# @File    : urls.py
# @Software: PyCharm
# @Description: urls
from django.conf import settings
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import LoginView, LogoutView, UserModelViewSet

router = routers.DefaultRouter()
router.register(r'user', UserModelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
