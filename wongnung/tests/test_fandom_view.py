from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from ..models.fandom import Fandom

from ..views.fandom import get_fandom


class TestFandomView(TestCase):
    """Tests for Fandom view"""

    def setUp(self):
        self.client = Client()
        self.fandom = Fandom.objects.create(name="MarvelFans")

    def test_get_fandom(self):
        """The function get_fandom should retrieve Fandom correctly"""
        valid_names = [
            "MarvelFans",
            "marvelfans",
            "MARVELFANS",
            "MaRvElFaNs",
            " MarvelFans ",
            "Marvel Fans",
        ]
        for name in valid_names:
            self.assertEqual(get_fandom(name), self.fandom)

    def test_show_fandom_template(self):
        """The view should have render the fandom template"""
        url = reverse("wongnung:fandom", args=(self.fandom.name,))
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, "wongnung/fandom_page.html")
