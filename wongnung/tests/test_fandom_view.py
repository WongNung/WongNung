import time
from unittest.mock import patch
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.humanize.templatetags.humanize import naturaltime

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

from ..models.film import Film
from ..models.review import Review
from ..models.fandom import Fandom
from ..views.fandom import get_fandom
from .utils import get_response_credits, get_response_info, new_test_user


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


class TestFandomE2E(StaticLiveServerTestCase):
    """End-to-end tests for Fandom view"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--log-level=3")
        cls.browser = Chrome(options=opts)
        cls.browser.implicitly_wait(3)
        cls.browser.set_page_load_timeout(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.client = Client()
        self.username = "Test"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)

        self.fandom_name = "NewFandom"

        # First GET makes Selenium recognize the domain
        self.browser.get(self.live_server_url + reverse("wongnung:feed"))
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:fandom", args=(self.fandom_name,))
        )

    def login(self):
        """Logins with test client then copies the cookie to Selenium"""
        self.client.login(username=self.username, password=self.password)
        cookie = self.client.cookies["sessionid"]
        self.browser.add_cookie(
            {
                "name": "sessionid",
                "value": cookie.value,
                "secure": False,
                "path": "/",
            }
        )
        self.browser.refresh()

    def test_fandom_visiting(self):
        """Fandom page is visited with correct fandom name"""
        self.assertEqual(
            f"#{self.fandom_name}",
            self.browser.find_element(By.ID, "fandomName").text,
        )

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_review_is_in_fandom(self):
        """There is a review with fandom tag in its text, it should be in fandom"""
        film = Film.get_film("0")
        review = Review.objects.create(
            film=film,
            content=f"This is a review for #{self.fandom_name}",
        )

        self.browser.refresh()

        self.assertIn(
            film.title,
            self.browser.find_element(
                By.CLASS_NAME, f"review{review.pk}"
            ).text,
        )

        self.assertIn(
            review.content,
            self.browser.find_element(
                By.CLASS_NAME, f"review{review.pk}"
            ).text,
        )

    def test_join_leave_fandom(self):
        """When joining or leaving fandom, it should update the join/leave button"""
        join_btn = self.browser.find_element(By.NAME, "join")
        self.assertTrue(join_btn)
        join_btn.click()

        leave_btn = self.browser.find_element(By.NAME, "leave")
        self.assertTrue(leave_btn)
        leave_btn.click()

        join_btn = self.browser.find_element(By.NAME, "join")
        self.assertTrue(join_btn)

    def test_member_count(self):
        """Member count is displayed correctly on fandom page"""
        self.assertIn(
            "0", self.browser.find_element(By.ID, "memberCount").text
        )
        join_btn = self.browser.find_element(By.NAME, "join")
        self.assertTrue(join_btn)
        join_btn.click()
        self.assertIn(
            "1", self.browser.find_element(By.ID, "memberCount").text
        )

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_last_active(self):
        """Last active in fandom should be displayed by recent review"""
        self.assertIn(
            "never", self.browser.find_element(By.ID, "lastActive").text
        )

        film = Film.get_film("0")
        review = Review.objects.create(
            film=film,
            content=f"This is a review for #{self.fandom_name}",
        )

        time.sleep(1)
        self.browser.refresh()

        self.assertIn(
            str(naturaltime(review.pub_date)),
            self.browser.find_element(By.ID, "lastActive").text,
        )

    # last active
