import time
from unittest.mock import patch
from selenium import webdriver
from django.test.client import Client
from selenium.webdriver.common.by import By
from wongnung.models.film import Film
from wongnung.models.review import Review
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .utils import get_response_credits, get_response_info, new_test_user


class BookmarkViewTest(StaticLiveServerTestCase):
    """End-to-end tests for bookmark view"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        cls.browser = webdriver.Chrome(options=options)
        cls.browser.implicitly_wait(30)
        cls.browser.set_page_load_timeout(30)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self) -> None:
        self.client = Client()
        self.username = "Test"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)
        self.film = Film.get_film("0")
        print(self.film.filmId)
        self.review = Review.objects.create(
            film=self.film, content="This is a review for #MatrixFans"
        )

    def login(self):
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

    def test_bookmark_film_color_change(self):
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:film-details", args=("0",))
        )
        # initial bookmark button color should be grey
        self.assertIn(
            "film0-bookmark-grey-tag",
            self.browser.find_element(By.CLASS_NAME, "film0-bookmark-button")
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        # after being clicked bookmark button color should be yellow
        self.browser.find_element(
            By.CLASS_NAME, "film0-bookmark-button"
        ).click()
        time.sleep(1)
        self.assertIn(
            "film0-bookmark-yellow-tag",
            self.browser.find_element(By.CLASS_NAME, "film0-bookmark-button")
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_bookmark_review_color_change(self):
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:film-details", args=("0",))
        )
        time.sleep(1)
        # initial bookmark button color should be grey
        self.assertIn(
            f"review{self.review.id}-bookmarked-text-tag-grey",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review.id}-bookmark-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        # after being clicked bookmark button color should be yellow
        self.browser.find_element(
            By.CLASS_NAME, f"review{self.review.id}-bookmark-button"
        ).click()
        time.sleep(1)
        self.assertIn(
            f"review{self.review.id}-bookmarked-text-tag-yellow",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review.id}-bookmark-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_bookmark_fandom_color_change(self):
        self.browser.get(self.live_server_url)
        self.login()
        time.sleep(1)
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:fandom", args=("MatrixFans",))
        )
        fandom_name = "MatrixFans"
        # initially bookmark button color should be grey
        self.assertIn(
            f"fandom{fandom_name}-bookmarked-text-tag-grey",
            self.browser.find_element(
                By.CLASS_NAME, f"fandom{fandom_name}-bookmark-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        # after being clicked bookmark button color should be yellow
        self.browser.find_element(
            By.CLASS_NAME, f"fandom{fandom_name}-bookmark-button"
        ).click()
        time.sleep(1)
        self.assertIn(
            f"fandom{fandom_name}-bookmarked-text-tag-yellow",
            self.browser.find_element(
                By.CLASS_NAME, f"fandom{fandom_name}-bookmark-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
