import io
import os

from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from buff_file import models
from buffdvp_django.settings import MEDIA_ROOT
from common.Mypagination import MyPageNumberPagination
from utils.MyResponse import MyResponse
from utils.path_utils import get_filepath_filename_extension
from .apps import BuffUserConfig as AppConfig
from .models import User
from .permissions import IsUser
from .serializers import UserSerializer, CreateUserSerializer, UserListSerializer, UserChangePasswordSerializer

app_config = apps.get_app_config(AppConfig.name)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    关闭csrf验证
    """

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

    def authenticate_header(self, request):
        return 'Session: Authentication credentials were not provided.'


class UserModelViewSet(viewsets.ModelViewSet):
    """
     A ViewSet for viewing and editing accounts.
    """
    queryset = User.objects.all()
    filter_backends = [OrderingFilter]
    ordering = ('-id',)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action == 'list':
            return UserListSerializer
        elif self.action == 'changePassword':
            return UserChangePasswordSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsUser]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.image.delete(save=False)
        instance.delete()

    def perform_create(self, serializer):
        serializer.save()
        path = os.path.join(MEDIA_ROOT, 'example', '示例表格.xlsx')
        with open(path, 'rb') as f:
            file = models.File(user=serializer.instance)
            file.file.save('示例表格.xlsx', File(f))
            file_url = file.file.name
            filepath, basename, extension = get_filepath_filename_extension(file_url)
            file.name = basename
            file.type = extension
            file.save()


    """
    修改密码
    """
    @action(methods=['post'], detail=True)
    def changePassword(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        old_password = serializer.validated_data['old_password']
        if not instance.check_password(old_password):
            raise ValidationError('旧密码不正确')
        instance.set_password(new_password)
        instance.save()
        return Response("密码修改成功", status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    用户登录 创建Session
    """
    permission_classes = (permissions.AllowAny,)

    authentication_classes = ()

    # throttle_scope = "requests"
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            data = {'id': user.id, 'username': user.username}
            return MyResponse(code=1, msg='登陆成功', data=data, status=status.HTTP_200_OK)
        return MyResponse(code=0, msg='登陆失败', status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    用户登出 清除Session
    """
    permission_classes = ()

    def delete(self, request, *args, **kwargs):
        username = request.user.username
        logout(request)
        data = {'username': username}
        return MyResponse(code=1, msg='登出成功', data=data, status=status.HTTP_200_OK)