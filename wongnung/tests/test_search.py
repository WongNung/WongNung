from unittest.mock import patch
from django.test import Client, TestCase
from django.urls import reverse


def empty_search_results():
    return {"results": []}


def search_results():
    return {
        "results": [
            {
                "id": 0,
                "title": "Test Movie",
                "release_date": "2022-01-01",
            },
            {
                "id": 1,
                "title": "Test Movie 2",
            },
        ]
    }


class TestSearch(TestCase):
    """Tests for search view"""

    def setUp(self):
        self.client = Client()

    def test_empty_string_search(self):
        """Empty search query should hide result box"""
        url = reverse("wongnung:search")
        resp = self.client.get(url, {"query": ""})
        self.assertContains(resp, "hidden")

    def test_short_string_search(self):
        """Search query with len < 3 should hide result box"""
        url = reverse("wongnung:search")
        resp = self.client.get(url, {"query": "ab"})
        self.assertContains(resp, "hidden")

    def test_search_with_results(self):
        """Searching should return a movie in the result box"""
        url = reverse("wongnung:search")
        with patch("tmdbsimple.Search.movie") as search:
            search.return_value = search_results()
            resp = self.client.get(url, {"query": "test"})
            self.assertContains(resp, "Test Movie (2022)")
            self.assertContains(resp, "Test Movie 2")

    def test_search_without_results(self):
        """If there's no result, hide the result box"""
        url = reverse("wongnung:search")
        with patch("tmdbsimple.Search.movie") as search:
            search.return_value = empty_search_results()
            resp = self.client.get(url, {"query": "test"})
            self.assertContains(resp, "hidden")

    def test_cancel_search(self):
        """When cancel_search is called, hide the result box"""
        url = reverse("wongnung:cancel-search")
        resp = self.client.get(url)
        self.assertContains(resp, "hidden")
