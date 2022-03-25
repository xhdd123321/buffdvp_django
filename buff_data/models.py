from django.contrib.auth import get_user_model
from django.db import models


class Chart(models.Model):
    # 表格标题
    title = models.CharField(max_length=255, blank=True, default="")
    # 表格表头
    header = models.JSONField(default=list, blank=True)
    # 表格内容
    body = models.JSONField(default=list, blank=True)
    # 用户
    user = models.ForeignKey(to=get_user_model(), blank=False, null=True, on_delete=models.CASCADE)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
