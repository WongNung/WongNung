"""Provided a test for bookmark module including Bookmark class and functions."""

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone

from ..models.bookmark import Bookmark, delete_bookmark, get_bookmark_set
from ..models.fandom import Fandom
from ..models.film import Film
from ..models.review import Review


class BookmarkModelTest(TestCase):
    """Contains test for Bookmark and functions."""

    def setUp(self):
        """2 film, 3 user, 2 review, 6 bookmarks created."""
        # create film
        self.film1 = Film.objects.create(filmId=1, title="Movie1")
        self.film2 = Film.objects.create(filmId=2, title="Movie1")
        # create user
        self.user1 = User.objects.create(
            username="Mr. Member1", email="user1@email.com", password="User1"
        )
        self.user2 = User.objects.create(
            username="Mr. Member2", email="user2@email.com", password="User2"
        )
        self.user3 = User.objects.create(
            username="Mr. Member3", email="user3@email.com", password="User3"
        )
        # create review
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
        self.review1 = Review.objects.create(
            film=self.film1,
            pub_date=timezone.now(),
            content="Nice Movies with great actors.",
            author=self.author1,
        )
        self.review2 = Review.objects.create(
            film=self.film2,
            pub_date=timezone.now(),
            content="Nice picture.",
            author=self.author2,
        )
        # create fandom
        self.fandom1 = Fandom.objects.create(name="MarvelFans")
        self.fandom2 = Fandom.objects.create(name="DCFans")
        # create bookmark
        self.bmk_film1 = Bookmark.objects.create(
            owner=self.user1, content_object=self.film1
        )
        self.bmk_film2 = Bookmark.objects.create(
            owner=self.user1, content_object=self.film2
        )
        self.bmk_review1 = Bookmark.objects.create(
            owner=self.user1, content_object=self.review1
        )

        self.bmk_review2 = Bookmark.objects.create(
            owner=self.user2, content_object=self.review1
        )
        self.bmk_fandom1 = Bookmark.objects.create(
            owner=self.user2, content_object=self.fandom1
        )

        self.bmk_fandom2 = Bookmark.objects.create(
            owner=self.user3, content_object=self.fandom2
        )
        # contenttype
        self.film_content_type = ContentType.objects.get(model="film")
        self.review_content_type = ContentType.objects.get(model="review")
        self.fandom_content_type = ContentType.objects.get(model="fandom")

    def test_bookmark_attribute(self):
        """Bookmark created holds correct information."""
        bookmark = Bookmark.objects.create(
            owner=self.user1, content_object=self.film1
        )
        self.assertEqual(self.user1, bookmark.owner)
        self.assertEqual(self.film1, bookmark.content_object)
        self.assertEqual(self.film1.filmId, bookmark.object_id)
        self.assertEqual(
            ContentType.objects.get(model="film"), bookmark.content_type
        )

    def test_get_bookmark_item_set(self):
        """Get bookmark should return correct bookmark items set."""
        expected_user1_film_bookmark_set = [self.bmk_film1, self.bmk_film2]
        self.assertListEqual(
            expected_user1_film_bookmark_set,
            list(
                get_bookmark_set(ct=self.film_content_type, owner=self.user1)
            ),
        )

        expected_user1_review_bookmark_set = [self.bmk_review1]
        self.assertListEqual(
            expected_user1_review_bookmark_set,
            list(
                get_bookmark_set(ct=self.review_content_type, owner=self.user1)
            ),
        )

        self.assertEqual(
            0,
            len(
                get_bookmark_set(ct=self.fandom_content_type, owner=self.user1)
            ),
        )

    def test_get_bookmark_independent(self):
        """Get bookmark should return user independently."""
        expected_user2_fandom_bookmark_set = [self.bmk_fandom1]
        self.assertListEqual(
            expected_user2_fandom_bookmark_set,
            list(
                get_bookmark_set(ct=self.fandom_content_type, owner=self.user2)
            ),
        )
        expected_user3_fandom_bookmark_set = [self.bmk_fandom2]
        self.assertListEqual(
            expected_user3_fandom_bookmark_set,
            list(
                get_bookmark_set(ct=self.fandom_content_type, owner=self.user3)
            ),
        )
        self.assertListEqual(
            expected_user2_fandom_bookmark_set,
            list(
                get_bookmark_set(ct=self.fandom_content_type, owner=self.user2)
            ),
        )
        self.assertListEqual(
            expected_user3_fandom_bookmark_set,
            list(
                get_bookmark_set(ct=self.fandom_content_type, owner=self.user3)
            ),
        )

    def test_delete_bookmark(self):
        """Delete bookmark should work correctly."""
        delete_bookmark(self.film_content_type, owner=self.user1, obj_id="2")
        expected_user1_bookmark_set = [self.bmk_film1, self.bmk_review1]
        self.assertListEqual(
            expected_user1_bookmark_set,
            list(Bookmark.objects.filter(owner=self.user1)),
        )

        delete_bookmark(
            self.fandom_content_type,
            owner=self.user3,
            obj_id=self.fandom2.name,
        )
        self.assertListEqual(
            [], list(Bookmark.objects.filter(owner=self.user3))
        )

    def test_delete_bookmark_independently(self):
        """Delete bookmark should be independently b/w user."""
        delete_bookmark(
            self.review_content_type, owner=self.user2, obj_id=self.review1.pk
        )
        expected_user1_bookmark_set = [
            self.bmk_film1,
            self.bmk_film2,
            self.bmk_review1,
        ]
        self.assertListEqual(
            expected_user1_bookmark_set,
            list(Bookmark.objects.filter(owner=self.user1)),
        )
