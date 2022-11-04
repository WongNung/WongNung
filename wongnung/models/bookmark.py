from __future__ import annotations

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db import models


class Bookmark(models.Model):
    """This class hold ContentType."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return f"Bookmark of {self.owner}"

    def get_item(self):
        """Get an item in a bookmark."""
        return self.content_object
