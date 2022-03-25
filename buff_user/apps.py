from django.apps import AppConfig


class BuffUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buff_user'
    verbose_name = '用户管理模块'

    # 用户头像存储 URL 规则
    @staticmethod
    def re_user_avatar(key):
        return 'avatars/avatar_{0}.png'.format(key)
