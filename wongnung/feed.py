import logging

import datetime
from typing import Any, Dict, List, Optional

from .models import CustomUser as User
from django.db.models import Q
from django.utils import timezone

from wongnung.insights import UserInsights

from .models.review import Review

logger = logging.getLogger(__name__)

user_insights = UserInsights()


class FeedSession:
    """A session for each user which contains a stack of content."""

    def __init__(self, user_id: int):
        try:
            self.user_id = User.objects.get(pk=user_id).pk
        except User.DoesNotExist:
            logger.warning(f"User with ID {user_id} does not exist.")
            raise

        self.stack: List[int] = [
            review.pk for review in self.gen_from_insights(user_id)
        ]

    def gen_from_insights(self, user_id: int):
        """Generate stack from insights"""
        user: User = User.objects.get(pk=user_id)
        insights = user_insights.get(user)

        if not insights:  # No insights yet
            logger.info(f"No insights found for user {user_id}. Returning all reviews ordered by publication date.")
            return Review.objects.all().order_by("-pub_date")

        accepts = Q()  # Q() that ensures criteria
        excludes = Q()  # Q() that excludes content

        for activity in insights[::-1]:
            if activity.accepts():
                accepts |= activity.accepts()
            if activity.excludes():
                excludes |= activity.excludes()

        logger.info(f"Generating feed from insights for user {user_id}.")
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
            logger.info(f"Feed stack is empty for user {self.user_id}.")
            return None

        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            logger.warning(f"Review with ID {pk} does not exist.")
            return None

    def save(self, manager: "FeedManager"):
        try:
            manager.update_feed_session(self.user_id, self)
        except Exception as e:
            logger.error(f"Error saving feed session for user {self.user_id}: {str(e)}")


    def __str__(self):
        return f"Feed {self.user_id}: {self.stack}"


class FeedManager:
    """
    A singleton manager class which manage feed sessions.
    This create new feed sessions, update existing sessions
    and remove expired sessions.
    """

    feeds: Dict[int, Any] = dict()
    MAX_DURATION: int = 5

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
                self.new_feed_session(user_id)
            return self.feeds[user_id]["feed"]
        except KeyError:
            logger.info(f"Creating new feed session for user {user_id} (no existing session found).")
            self.new_feed_session(user_id)
        return self.feeds[user_id]["feed"]

    def new_feed_session(self, user_id: int):
        """Creates a new feed session for user."""
        logger.info(f"Creating new feed session for user {user_id}.")
        self.feeds[user_id] = {
            "feed": FeedSession(user_id),
            "expiry": timezone.now()
            + datetime.timedelta(minutes=self.MAX_DURATION),
        }

    def update_feed_session(self, user_id: int, feed: FeedSession):
        """Updates existing feed session for user."""
        logger.info(f"Updating feed session for user {user_id}.")
        self.feeds[user_id] = {
            "feed": feed,
            "expiry": timezone.now()
            + datetime.timedelta(minutes=self.MAX_DURATION),
        }
