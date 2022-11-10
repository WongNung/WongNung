from __future__ import annotations
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    display_name = models.CharField(max_length=32, blank=True)
    color = models.CharField(max_length=6, default="D9D9D9")

    def __str__(self):
        return f""
