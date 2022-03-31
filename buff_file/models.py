import os

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

from utils.path_utils import get_filepath_filename_extension
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

@receiver(post_delete, sender=File)
def delete_upload_files(sender, instance, **kwargs):
        file = getattr(instance, 'file', '')
        if not file:
            return
        filepath, filename, extension = get_filepath_filename_extension(file.path)
        file.delete(save=False)
        if os.path.isdir(filepath) and not os.listdir(filepath):
            os.rmdir(filepath)
