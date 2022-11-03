from unittest.mock import patch
from django.test import Client, TestCase
from django.urls import reverse
from ..models.film import Film

from .utils import (
    get_response_credits,
    get_response_info,
    new_test_user,
)


class TestFilmDetailsView(TestCase):
    """Tests for Film details view"""

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.client = Client()
        self.username = "Test"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)
        self.film = Film.get_film("0")

    def test_render_film_details(self):
        """Tests if the page is using film details template"""
        self.client.login(username=self.username, password=self.password)
        url = reverse("wongnung:film-details", args=(self.film.pk,))
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, "wongnung/film_details_page.html")

    def test_correct_film_details(self):
        """Tests if the film has correct details"""
        self.client.login(username=self.username, password=self.password)
        url = reverse("wongnung:film-component", args=(self.film.pk,))
        resp = self.client.get(url)
        self.assertContains(resp, self.film.title)
        self.assertContains(resp, str(self.film.year_released))
        self.assertContains(resp, self.film.summary)
