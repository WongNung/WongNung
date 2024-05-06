from __future__ import annotations
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """
    A model that represents profile settings for each user
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    display_name = models.CharField(max_length=32, blank=True)
    _color = models.CharField(max_length=6, default="D9D9D9")

    def __str__(self):
        return f"User Profile of {self.user.username}"

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str):
        self._color = color
