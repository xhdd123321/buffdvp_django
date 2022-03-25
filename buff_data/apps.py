from django.apps import AppConfig


class BuffDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buff_data'
    verbose_name = '基础数据模块'

    # 自定义配置
    debug = True
