from django.apps import apps
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from buff_user.permissions import IsOwner
from common.Mypagination import MyPageNumberPagination
from .apps import BuffFileConfig as AppConfig
from .filters import IsOwnerFilterBackend
from .models import File
from .serializers import FileCreateSerializers, FileSerializers

app_config = apps.get_app_config(AppConfig.name)


class FileModelViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    """
    文件管理 API （不包括更新）
    """

    queryset = File.objects.all()
    filter_backends = [IsOwnerFilterBackend, OrderingFilter]
    ordering = ('id',)
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return FileCreateSerializers
        else:
            return FileSerializers

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.file is not None:
            instance.file.delete(save=False)
        instance.delete()
