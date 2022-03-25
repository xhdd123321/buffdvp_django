#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/3/19 17:04
# @Author  : 10711
# @File    : statistics_utils.py
# @Software: PyCharm
# @Description: time_utils
import datetime
import platform

import psutil
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

START_TIME = '2022-3-18'


def get_site_runtime():
    start_time = datetime.datetime.strptime(START_TIME, '%Y-%m-%d')
    now_time = datetime.datetime.now()
    runtime = (now_time - start_time).days
    return runtime


def get_site_onlineCount():
    sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
    user_list = []
    for session in sessions:
        data = session.get_decoded()
        user_list.append(data.get('_auth_user_id', None))
    return len(set(user_list))


def get_registered_count():
    count = get_user_model().objects.all().count()
    return count


def get_sys_info():
    info_res = {
        'platform': platform.platform()
    }
    return info_res


def get_cpu_info():
    # 显示cpu所有逻辑信息
    # print(psutil.cpu_times(percpu=True))
    # 查看cpu逻辑个数的信息
    count_logical = psutil.cpu_count()
    # print(u"逻辑CPU个数: %s" % count_logical)
    # 查看cpu物理个数的信息
    count_phy = psutil.cpu_count(logical=False)
    # print(u"物理CPU个数: %s" % count_phy)
    # CPU的使用率
    percent = psutil.cpu_percent(1)
    # cpu = (str(psutil.cpu_percent(1))) + '%'
    # print(u"cup使用率: %s" % cpu)
    info_res = {
        'count_logical': count_logical,
        'count_phy': count_phy,
        'percent': percent
    }
    return info_res


def get_net_info():
    # 获取网络总IO信息
    # print(psutil.net_io_counters())
    # 发送数据包
    bytes_sent = psutil.net_io_counters().bytes_sent
    # print("发送数据字节:", psutil.net_io_counters().bytes_sent, "bytes")
    # 接收数据包
    bytes_recv = psutil.net_io_counters().bytes_recv
    # print("接收数据字节:", psutil.net_io_counters().bytes_recv, "bytes")
    info_res = {
        'bytes_sent': bytes_sent,
        'bytes_recv': bytes_recv
    }
    return info_res


def get_mem_info():
    # 内存
    mem = psutil.virtual_memory()
    # 系统总计内存
    total = float(mem.total) / 1024 / 1024 / 1024
    # 系统已经使用内存
    used = float(mem.used) / 1024 / 1024 / 1024
    # 系统空闲内存
    free = float(mem.free) / 1024 / 1024 / 1024
    # print('系统总计内存:%d.4GB' % total)
    # print('系统已经使用内存:%d.4GB' % used)
    # print('系统空闲内存:%d.4GB' % free)
    info_res = {
        'total': round(total, 1),
        'used': round(used, 1),
        'free': round(free, 1)
    }
    return info_res
