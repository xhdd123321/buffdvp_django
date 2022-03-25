from django.apps import AppConfig


class BuffEchartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buff_echart'
    verbose_name = 'echart处理模块'

    # 自定义配置
    debug = True

