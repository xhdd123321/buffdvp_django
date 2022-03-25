from django.apps import AppConfig


class BuffFileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buff_file'
    verbose_name = '文件管理模块'

    # 文件存储 URL 规则
    @staticmethod
    def re_file(key, filename):
        return 'files/{0}/{1}'.format(key, filename)
