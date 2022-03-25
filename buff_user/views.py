from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from common.Mypagination import MyPageNumberPagination
from utils.MyResponse import MyResponse
from .apps import BuffUserConfig as AppConfig
from .models import User
from .permissions import IsUser
from .serializers import UserSerializer, CreateUserSerializer, UserListSerializer

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