#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 13:41
# @Author  : 10711
# @File    : filters.py
# @Software: PyCharm
# @Description: filters
from rest_framework import filters


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        if view.action == 'list' and not request.user.is_superuser:
            return queryset.filter(user=request.user)
        return queryset
