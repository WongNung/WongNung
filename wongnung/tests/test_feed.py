import datetime
from unittest.mock import patch
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from ..feed import FeedSession, FeedManager


def get_placeholder_time(offset_minutes: int = 0):
    return timezone.datetime(
        2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
    ) + datetime.timedelta(minutes=offset_minutes)


class TestFeedSession(TestCase):
    pass


@patch("django.utils.timezone.now", new=get_placeholder_time)
class TestFeedManager(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Test")
        self.manager = FeedManager()

    def test_is_singleton(self):
        """FeedManager should be a singleton"""
        other_manager = FeedManager()
        self.assertIs(self.manager, other_manager)

    def test_feed_session_not_exists(self):
        """If a FeedSession for a user does not exists, create a new one"""
        self.assertEqual(len(self.manager.feeds), 0)
        session = self.manager.get_feed_session(self.user.pk)
        self.assertEqual(len(self.manager.feeds), 1)
        self.assertIn(
            (self.user.pk, {"feed": session, "expiry": get_placeholder_time(5)}), self.manager.feeds.items()
        )

    def test_feed_update(self):
        """If a FeedSession has elapsed but not expired, update the FeedSession"""
        self.assertEqual(len(self.manager.feeds), 0)
        session = self.manager.get_feed_session(self.user.pk)
        self.assertIn(
            (self.user.pk, {"feed": session, "expiry": get_placeholder_time(5)}), self.manager.feeds.items()
        )
        with patch("django.utils.timezone.now") as now:
            now.return_value = get_placeholder_time(1)
            session = self.manager.get_feed_session(self.user.pk)
            self.assertEqual(len(self.manager.feeds), 1)
            self.assertIn(
                (self.user.pk, {"feed": session, "expiry": get_placeholder_time(6)}), self.manager.feeds.items()
            )

    def tearDown(self):
        self.manager.feeds.clear()
        del FeedManager.instance # Destroy manager before starting new tests
