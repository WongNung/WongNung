import datetime
from typing import List, Optional

from django.contrib.auth.models import User
from django.utils import timezone

from .models import Review


class FeedSession:
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


class FeedManager:

    feeds = dict()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(FeedManager, cls).__new__(cls)
        return cls.instance

    def get_feed_session(self, user_id: int) -> FeedSession:
        try:
            feed_data = self.feeds[user_id]
            if (timezone.now() > feed_data["expiry"]) or (
                not feed_data["feed"].stack
            ):
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
        self.feeds[user_id] = {
            "feed": feed,
            "expiry": timezone.now() + datetime.timedelta(minutes=5),
        }
