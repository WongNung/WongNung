from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.db.models.functions import Lower
from django.conf import settings


class Fandom(models.Model):
    """A model as group of users with specific tag"""

    name = models.CharField(max_length=64, primary_key=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="members")

    class Meta:
        """Create unique constraint on lowercase value of name as PK."""

        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="fandom_name_unique"  # type: ignore
            )
        ]

    def __str__(self):
        return f"Fandom for {self.name}"

    def add_member(self, new_member: settings.AUTH_USER_MODEL):
        """Add new member to a fandom."""
        self.members.add(new_member)

    def remove_member(self, existing_member:  settings.AUTH_USER_MODEL,):
        """Remove existing member from a fandom."""
        self.members.remove(existing_member)

    def get_member_count(self) -> int:
        """Return total number of members."""
        return self.members.all().count()

    def get_all_member(self) -> QuerySet[ settings.AUTH_USER_MODEL,]:
        """Return queryset of members."""
        return self.members.all()
