from __future__ import annotations

from django.contrib.auth.models import User
from .film import Film
from django.db import models
from django.utils import timezone


class Review(models.Model):
    """
    Model for Review with Film object and publishing date

    :param film: A Film object
    :type film: Film
    :param pub_date: A date object representing the published date of the review
    :type pub_date: Datetime
    :param content: A string representation of the content of this Review
    :type content: str
    :param author: User who created the Review
    :type author: User
    """

    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    upvotes = models.ManyToManyField(User, related_name="upvotes")
    downvotes = models.ManyToManyField(User, related_name="downvotes")

    def __str__(self) -> str:
        string = f"Review for {self.film} @ {self.pub_date}"
        if self.author:
            return string + f" by {self.author}"
        return string + " by anonymous"

    def get_votes(self) -> int:
        """Get number of upvotes minus downvotes."""
        return self.get_upvotes() - self.get_downvotes()

    def get_upvotes(self) -> int:
        """Get number of upvotes."""
        return self.upvotes.all().count()

    def get_downvotes(self) -> int:
        """Get number of downvotes."""
        return self.downvotes.all().count()

    def add_upvotes(self, user: User):
        """Add User to upvotes."""
        self.upvotes.add(user)

    def remove_upvotes(self, user: User):
        """Remove User from upvotes."""
        self.upvotes.remove(user)

    def add_downvotes(self, user: User):
        """Add User to downvotes."""
        self.downvotes.add(user)

    def remove_downvotes(self, user: User):
        """Remove User from downvotes."""
        self.downvotes.remove(user)
