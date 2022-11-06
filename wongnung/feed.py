import datetime
from typing import List, Optional

from django.contrib.auth.models import User
from django.utils import timezone

from .models.review import Review


class FeedSession:
    """A session for each user which contains a stack of content."""

    def __init__(self, user_id: int):
        try:
            self.user_id = User.objects.get(pk=user_id).pk
        except User.DoesNotExist:
            raise

        # TODO: Make stack more personalized in future...
        self.stack: List[int] = sorted(
            [review.pk for review in Review.objects.all()], reverse=True
        )

    def pop(self) -> Optional[Review]:
        """
        Take and return Review object from the stack,
        if the stack is empty, return None.
        """
        try:
            pk = self.stack.pop(0)
        except IndexError:
            return None

        return Review.objects.get(pk=pk)

    def save(self, manager: "FeedManager"):
        manager.update_feed_session(self.user_id, self)

    def __str__(self):
        return f"Feed {self.user_id}: {self.stack}"


class FeedManager:
    """
    A singleton manager class which manage feed sessions.
    This create new feed sessions, update existing sessions
    and remove expired sessions.
    """

    feeds = dict()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(FeedManager, cls).__new__(cls)
        return cls.instance

    def get_feed_session(
        self, user_id: int, renew: bool = True
    ) -> FeedSession:
        """
        Retreive feed session for user.
        If feed for the user doesn't exist, create a new one.
        If feed expires, create a new one.
        If renew=True, create a new one.
        """
        try:
            feed_data = self.feeds[user_id]
            if (
                (timezone.now() > feed_data["expiry"])
                or (not feed_data["feed"].stack)
            ) and renew:
                self.feeds[user_id] = {
                    "feed": FeedSession(user_id),
                    "expiry": timezone.now() + datetime.timedelta(minutes=5),
                }
            return self.feeds[user_id]["feed"]
        except KeyError:
            self.feeds[user_id] = {
                "feed": FeedSession(user_id),
                "expiry": timezone.now() + datetime.timedelta(minutes=5),
            }
        return self.feeds[user_id]["feed"]

    def update_feed_session(self, user_id: int, feed: FeedSession):
        """Updates existing feed session for user."""
        self.feeds[user_id] = {
            "feed": feed,
            "expiry": timezone.now() + datetime.timedelta(minutes=5),
        }
