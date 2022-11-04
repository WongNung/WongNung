from __future__ import annotations
from typing import Union
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from .review import Review
from .film import Film
from .fandom import Fandom


def get_bookmark_set(ct: ContentType, owner: User) -> QuerySet[Bookmark]:
    """Get bookmarks for certain user with specified type."""
    return Bookmark.objects.filter(content_type=ct, owner=owner)


def delete_bookmark(ct: ContentType, owner: User, obj_id: int):
    """Delete a specified bookmark."""
    Bookmark.objects.filter(content_type=ct, owner=owner, object_id=obj_id).delete()


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
