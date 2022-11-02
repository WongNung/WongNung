import datetime
from unittest.mock import patch
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from ..models.film import Film
from ..models.review import Review
from ..feed import FeedSession, FeedManager
from .utils import get_response_info, get_response_credits


def get_placeholder_time(offset_minutes: int = 0):
    return timezone.datetime(
        2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
    ) + datetime.timedelta(minutes=offset_minutes)


class TestFeedSession(TestCase):
    """Tests for FeedSession class"""

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.user = User.objects.create(username="Test")
        self.film = Film.get_film("0")
        self.review = Review.objects.create(
            film=self.film, content="", author=self.user
        )

    def test_init_no_user(self):
        """If there's no User with ID, raise DoesNotExist"""
        with self.assertRaises(User.DoesNotExist):
            FeedSession(self.user.pk + 999)

    def test_pop(self):
        """Popping from non-empty FeedSession once should return a Review object"""
        session = FeedSession(self.user.pk)
        review = session.pop()
        self.assertEqual(self.review, review)

    def test_pop_empty(self):
        """Popping from empty FeedSession should return None"""
        session = FeedSession(self.user.pk)
        session.pop()
        review = session.pop()
        self.assertIsNone(review)

    def test_save_session(self):
        """Saving a FeedSession should be correct"""
        manager = FeedManager()
        session = manager.get_feed_session(self.user.pk)
        self.assertEqual(len(session.stack), 1)
        session.stack += [999]
        session.save(manager)

        session = manager.get_feed_session(self.user.pk)
        self.assertEqual(len(session.stack), 2)

        manager.feeds.clear()
        del FeedManager.instance


@patch("django.utils.timezone.now", new=get_placeholder_time)
class TestFeedManager(TestCase):
    """Tests for FeedManager class"""

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
            (
                self.user.pk,
                {"feed": session, "expiry": get_placeholder_time(5)},
            ),
            self.manager.feeds.items(),
        )

    def test_feed_update(self):
        """If a FeedSession has elapsed but not expired, update the FeedSession"""
        self.assertEqual(len(self.manager.feeds), 0)
        session = self.manager.get_feed_session(self.user.pk)
        self.assertIn(
            (
                self.user.pk,
                {"feed": session, "expiry": get_placeholder_time(5)},
            ),
            self.manager.feeds.items(),
        )
        with patch("django.utils.timezone.now") as now:
            now.return_value = get_placeholder_time(1)
            session = self.manager.get_feed_session(self.user.pk)
            self.assertEqual(len(self.manager.feeds), 1)
            self.assertIn(
                (
                    self.user.pk,
                    {"feed": session, "expiry": get_placeholder_time(6)},
                ),
                self.manager.feeds.items(),
            )

    def test_expired_feed(self):
        """If a FeedSession has expired, the FeedSession should be recreated"""
        session = self.manager.get_feed_session(self.user.pk)
        with patch("django.utils.timezone.now") as now:
            now.return_value = get_placeholder_time(10)
            new_session = self.manager.get_feed_session(self.user.pk)
            self.assertEqual(len(self.manager.feeds), 1)
            self.assertIn(
                (
                    self.user.pk,
                    {"feed": new_session, "expiry": get_placeholder_time(15)},
                ),
                self.manager.feeds.items(),
            )
            self.assertIsNot(session, new_session)

    def test_update_feed_session(self):
        """Test the function `update_feed_session`
        to see if the feed session is updated correctly"""
        session = self.manager.get_feed_session(self.user.pk)
        session.stack += [999]
        self.manager.update_feed_session(self.user.pk, session)
        self.assertIn(999, self.manager.get_feed_session(self.user.pk).stack)

    def tearDown(self):
        self.manager.feeds.clear()
        del FeedManager.instance  # Destroy manager before starting new tests
