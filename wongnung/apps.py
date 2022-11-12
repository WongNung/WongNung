from django.apps import AppConfig


class WongnungConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wongnung"

    def ready(self) -> None:
        pre_social_login.connect(callback)
