from django.apps import AppConfig
from allauth.socialaccount.signals import pre_social_login


def callback(sender, **kwargs):
    print(sender)
    print([*kwargs])


class WongnungConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wongnung"

    def ready(self) -> None:
        pre_social_login.connect(callback)
