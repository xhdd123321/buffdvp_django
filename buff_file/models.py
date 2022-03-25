from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .apps import BuffFileConfig as BuffConfig
from django.db import models


def user_directory_path(instance, filename):
    return BuffConfig.re_file(instance.user.username, filename)


class File(models.Model):
    # 文件名
    name = models.CharField(max_length=255, blank=True, default="")
    # 文件类型
    type = models.CharField(max_length=255, blank=True, default="")
    # 文件 URL
    file = models.FileField(max_length=100, blank=False, null=True, upload_to=user_directory_path)
    # 用户
    user = models.ForeignKey(to=get_user_model(), blank=False, null=True, on_delete=models.CASCADE)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
