"""Tests for Review model"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..tests.utils import get_response_info, get_response_credits, MATRIX
from ..models.film import Film
from ..models.review import Review


class ReviewModelTests(TestCase):
    """This class test behaviours and functionalities of Review model."""

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.film = Film.get_film(MATRIX)
        self.author1 = User.objects.create(
            username="Mr. AuthorOne",
            email="author1@email.com",
            password="Author1",
        )
        self.author2 = User.objects.create(
            username="Mr. AuthorTwo",
            email="author2@email.com",
            password="Author2",
        )
        self.user1 = User.objects.create(
            username="Mr. User1", email="user1@email.com", password="User1"
        )
        self.user2 = User.objects.create(
            username="Mr. User2", email="user2@email.com", password="User2"
        )
        self.user3 = User.objects.create(
            username="Mr. User3", email="user3@email.com", password="User3"
        )
        self.user4 = User.objects.create(
            username="Mr. User4", email="user4@email.com", password="User4"
        )
        self.review1 = Review.objects.create(
            film=self.film,
            pub_date=timezone.now(),
            content="Nice Movies with great actors.",
            author=self.author1,
        )
        self.review2 = Review.objects.create(
            film=self.film,
            pub_date=timezone.now(),
            content="Nice picture.",
            author=self.author2,
        )

    def test_add_upvotes(self):
        """Add upvotes functionality work."""
        self.review1.add_upvotes(self.user1)
        self.assertEqual(1, self.review1.upvotes.all().count())
        self.review1.add_upvotes(self.user2)
        self.assertEqual(2, self.review1.upvotes.all().count())

    def test_add_downvotes(self):
        """Add downvotes functionality work."""
        self.review1.add_downvotes(self.user1)
        self.assertEqual(1, self.review1.downvotes.all().count())
        self.review1.add_downvotes(self.user2)
        self.assertEqual(2, self.review1.downvotes.all().count())

    def test_upvotes_downvotes_independent_between_review(self):
        """Upvotes and downvotes should be independent between reviews."""
        self.review1.add_upvotes(self.user1)
        self.review1.add_upvotes(self.user2)
        self.review2.add_downvotes(self.user1)
        self.assertEqual(2, self.review1.upvotes.all().count())
        self.assertEqual(1, self.review2.downvotes.all().count())

    def test_remove_votes(self):
        """Remove upvotes and downvotes functionality work."""
        self.review1.add_upvotes(self.user1)
        self.review1.remove_upvotes(self.user1)
        self.assertEqual(0, self.review1.upvotes.all().count())
        self.review1.add_downvotes(self.user3)
        self.review1.add_downvotes(self.user4)
        self.review1.remove_downvotes(self.user3)
        self.assertEqual(1, self.review1.downvotes.all().count())
        self.review1.remove_downvotes(self.user4)
        self.assertEqual(0, self.review1.downvotes.all().count())

    def test_get_upvotes_downvotes(self):
        """Get upvotes and downvotes functionality work."""
        self.review1.add_upvotes(self.user1)
        self.review1.add_upvotes(self.user2)
        self.review1.add_downvotes(self.user3)
        self.assertEqual(2, self.review1.get_upvotes())
        self.assertEqual(1, self.review1.get_downvotes())

    def test_get_votes(self):
        """Get votes functionality work."""
        self.review1.add_upvotes(self.user1)
        self.review1.add_upvotes(self.user2)
        self.review1.add_downvotes(self.user3)
        self.assertEqual(1, self.review1.get_votes())
