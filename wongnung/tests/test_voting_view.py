from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from ..models.film import Film
from ..models.review import Review
from .utils import get_response_credits, get_response_info, new_test_user


class TestVotingView(TestCase):
    """Tests for Voting view"""

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.client = Client()
        self.username = "Test"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)
        self.film = Film.get_film("0")
        self.review = Review.objects.create(
            film=self.film, content="", author=self.user
        )
        self.client.login(username=self.username, password=self.password)

    def test_vote_redirects(self):
        """Voting will refresh the review component"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        resp = self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertRedirects(
            resp, reverse("wongnung:review-component", args=(self.review.pk,))
        )

    def test_upvote_once(self):
        """Upvoting once should only add 1 to upvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 1)
        self.assertEqual(self.review.get_downvotes(), 0)

    def test_downvote_once(self):
        """Downvoting once should only add 1 to downvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 1)

    def test_upvote_twice(self):
        """Upvoting twice should remove existing upvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 0)

    def test_downvote_twice(self):
        """Downvoting twice should remove existing downvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 0)

    def test_alternate_vote(self):
        """Once upvoted, then downvote it should remove the upvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 1)
        self.assertEqual(self.review.get_downvotes(), 0)
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 1)
