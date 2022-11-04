from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet


class Fandom(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return f"Group's name is {self.name}"

    def add_member(self, new_member: User):
        """Add new member to a fandom."""
        self.members.add(new_member)

    def remove_member(self, existing_member: User):
        """Remove existing member from a fandom."""
        self.members.remove(existing_member)

    def get_member_count(self) -> int:
        """Return total number of members."""
        return self.members.all().count()

    def get_all_member(self) -> QuerySet[User]:
        """Return queryset of members."""
        return self.members.all()
