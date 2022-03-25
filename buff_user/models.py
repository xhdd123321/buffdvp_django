import os
import pathlib

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage
from django.core.files.utils import validate_file_name
from django.db import models

from .apps import BuffUserConfig as BuffConfig
from rest_framework.authtoken.models import Token


class Gender(models.TextChoices):
    MALE = '男',
    FEMALE = '女',
    UNKNOWN = '未知',


class UserType(models.IntegerChoices):
    USER = 0,
    ADMIN = 1,


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatars/avatar_user_<username>.png
    return BuffConfig.re_user_avatar(instance.username)


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        name = str(name).replace('\\', '/')
        dir_name, file_name = os.path.split(name)
        if '..' in pathlib.PurePath(dir_name).parts:
            raise SuspiciousFileOperation("Detected path traversal attempt in '%s'" % dir_name)
        validate_file_name(file_name)

        if self.exists(name):
            self.delete(name)

        return name


class User(AbstractUser):
    # 昵称
    nick_name = models.CharField(max_length=255, blank=True, default='未设置昵称')
    # 性别
    gender = models.CharField(max_length=8, choices=Gender.choices, default=Gender.UNKNOWN)
    # 手机号
    mobile = models.CharField(max_length=11, blank=True, default='')
    # 头像
    image = models.ImageField(max_length=100, null=True, upload_to=user_directory_path, storage=OverwriteStorage())
    # 用户类型
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.USER)

    def __str__(self):
        return self.username
