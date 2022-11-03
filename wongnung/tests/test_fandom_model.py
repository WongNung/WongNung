"""Tests for Fandom model"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from ..tests.utils import get_response_info, get_response_credits, MATRIX
from ..models import Film, Fandom


class FandomModelTests(TestCase):
    """This class test behaviours and functionalities of Fandom model."""

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.film = Film.get_film(MATRIX)
        self.owner = User.objects.create(
            username='Mr. Owner', email='owner1@email.com', password='Owner1')
        self.user1 = User.objects.create(
            username='Mr. Member1', email='user1@email.com', password='User1')
        self.user2 = User.objects.create(
            username='Mr. Member2', email='user2@email.com', password='User2')
        self.user3 = User.objects.create(
            username='Mr. Member3', email='user3@email.com', password='User3')
        self.user4 = User.objects.create(
            username='Mr. Member4', email='user4@email.com', password='User4')
        self.fandom1 = Fandom.objects.create(name='Marvel Fans')

    def test_add_member(self):
        """add_member() functionality work."""
        self.fandom1.add_member(self.owner)
        self.assertEqual(1, self.fandom1.members.all().count())

        # add more members
        self.fandom1.add_member(self.user1)
        self.fandom1.add_member(self.user2)
        self.fandom1.add_member(self.user3)
        self.assertEqual(4, self.fandom1.members.all().count())

    def test_remove_member(self):
        """remove_member() functionality work."""
        self.fandom1.add_member(self.owner)
        self.fandom1.add_member(self.user1)
        self.fandom1.remove_member(self.user1)
        self.assertEqual(1, self.fandom1.members.all().count())

    def test_get_member_count(self):
        """get_member_count() should return the correct number of members in fandom."""
        self.fandom1.add_member(self.owner)
        self.fandom1.add_member(self.user1)
        self.fandom1.add_member(self.user2)
        self.assertEqual(3, self.fandom1.get_member_count())

        # add more members
        self.fandom1.add_member(self.user3)
        self.assertEqual(4, self.fandom1.get_member_count())

    def test_get_all_member(self):
        """get_all_member() should return correct queryset of members."""
        self.fandom1.add_member(self.owner)
        self.fandom1.add_member(self.user1)
        self.fandom1.add_member(self.user2)

        # check only members in QuerySet not order
        expected = self.fandom1.members.all().order_by('username')
        method_output = self.fandom1.get_all_member().order_by('username')
        self.assertQuerysetEqual(expected, method_output)
