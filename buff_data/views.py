import datetime

from django.apps import apps
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework.views import APIView

from buff_user.permissions import IsOwner
from common.Mypagination import MyPageNumberPagination
from utils.statistics_utils import get_site_runtime, get_site_onlineCount, get_registered_count, get_cpu_info, \
    get_net_info, get_mem_info, get_sys_info
from .filters import IsOwnerFilterBackend
from .apps import BuffDataConfig as AppConfig
from rest_framework import mixins, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Chart
from .serializers import ChartCreateSerializers, ChartSerializers, ChartListSerializers

app_config = apps.get_app_config(AppConfig.name)


class ChartModelViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """
    标准图表管理 API （不包括更新）
    """

    queryset = Chart.objects.all()
    filter_backends = [IsOwnerFilterBackend, OrderingFilter]
    ordering = ('id',)
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return ChartCreateSerializers
        elif self.action == 'list':
            return ChartListSerializers
        else:
            return ChartSerializers

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DashBoardView(APIView):
    """
    获取 仪表盘数据
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # 获取站点信息
        siteInfo = {
            'onlineCount': get_site_onlineCount(),
            'registeredCount': get_registered_count(),
            'siteRuntime': get_site_runtime()
        }
        # 获取cpu信息
        cpuInfo = get_cpu_info()
        # 获取网络信息
        netInfo = get_net_info()
        # 获取内存信息
        memInfo = get_mem_info()
        # 获取系统信息
        sysInfo = get_sys_info()
        data = {
            'siteInfo': siteInfo,
            'cpuInfo': cpuInfo,
            'netInfo': netInfo,
            'memInfo': memInfo,
            'sysInfo': sysInfo
        }
        return Response(data, status=status.HTTP_200_OK)
