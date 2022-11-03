from unittest.mock import patch
from django.test import Client, TestCase
from django.urls import reverse
from ..feed import FeedManager
from ..models.film import Film
from ..models.review import Review

from .utils import (
    get_response_credits,
    get_response_info,
    new_test_user,
)


class TestFeedView(TestCase):
    """Tests for Feed view"""

    def setUp(self):
        self.client = Client()
        self.username = "Test"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)
        self.manager = FeedManager()
        self.client.login(username=self.username, password=self.password)

    def test_render_feed_page(self):
        """Tests if the page is using feed template"""
        url = reverse("wongnung:feed")
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, "wongnung/feed.html")

    def test_empty_feed(self):
        """If there is no content for FeedSession, it should return 'The end.'"""
        url = reverse("wongnung:get-feed")
        resp = self.client.get(url)
        self.assertContains(
            resp,
            """<span class="text-center text-white text-xl">The end.</span>""",
        )

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_entry_feed(self):
        """A FeedSession content should redirect to review component"""
        film = Film.get_film("0")
        review = Review.objects.create(film=film, content="", author=self.user)
        url = reverse("wongnung:get-feed")
        resp = self.client.get(url)
        self.assertRedirects(
            resp,
            reverse("wongnung:review-component", args=(review.pk,))
            + "?feed=true",
        )

    def tearDown(self):
        self.manager.feeds.clear()
        del FeedManager.instance  # Destroy manager before starting new tests
