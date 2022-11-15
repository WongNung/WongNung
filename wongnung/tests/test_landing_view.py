from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class TestLandingView(TestCase):
    """Test for landing page"""

    def test_render_landing(self):
        """Landing page view should render correct template"""
        client = Client()
        resp = client.get(reverse("wongnung:landing"))
        self.assertTemplateUsed(resp, "wongnung/landing_page.html")
