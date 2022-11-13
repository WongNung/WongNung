import datetime
from typing import Any, Dict, List, Optional

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone

from wongnung.insights import UserInsights

from .models.review import Review

user_insights = UserInsights()


class FeedSession:
    """A session for each user which contains a stack of content."""

    def __init__(self, user_id: int):
        try:
            self.user_id = User.objects.get(pk=user_id).pk
        except User.DoesNotExist:
            raise

        self.stack: List[int] = [
            review.pk for review in self.gen_from_insights(user_id)
        ]

    def gen_from_insights(self, user_id: int):
        """Generate stack from insights"""
        user: User = User.objects.get(pk=user_id)
        insights = user_insights.get(user)

        if not insights:  # No insights yet
            return Review.objects.all().order_by("-pub_date")

        accepts = Q()  # Q() that ensures criteria
        excludes = Q()  # Q() that excludes content

        for activity in insights:
            if activity.accepts():
                accepts |= activity.accepts()
            if activity.excludes():
                excludes |= activity.excludes()

        return Review.objects.all().exclude(excludes) | Review.objects.filter(
            accepts
        ).exclude(excludes)

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

    feeds: Dict[int, Any] = dict()

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
