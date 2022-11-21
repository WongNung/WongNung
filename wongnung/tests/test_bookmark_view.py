import time
from unittest.mock import patch
from selenium import webdriver
from django.test.client import Client
from selenium.webdriver.common.by import By
from wongnung.models.film import Film
from wongnung.models.review import Review
from wongnung.models.fandom import Fandom
from wongnung.models.bookmark import Bookmark, delete_bookmark
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .utils import get_response_credits, get_response_info, new_test_user


class BookmarkViewTest(StaticLiveServerTestCase):
    """End-to-end tests for bookmark view"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
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
        self.username = "user1"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)
        self.film_id = "0"
        self.film = Film.get_film(self.film_id)
        self.fandom_name = "MatrixFans"
        self.review = Review.objects.create(
            film=self.film, content=f"This is a review for #{self.fandom_name}"
        )
        self.fandom = Fandom.objects.create(name=self.fandom_name)

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
        """Test film bookmark button color behavior."""
        # login and go to film detail page
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:film-details", args=(self.film_id,))
        )
        bookmark_button_class_name = f"film{self.film_id}-bookmark-button"
        # initial bookmark button color should be grey
        self.assertIn(
            f"film{self.film_id}-bookmark-grey-tag",
            self.browser.find_element(
                By.CLASS_NAME, bookmark_button_class_name
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        # after being clicked bookmark button color should be yellow
        self.browser.find_element(
            By.CLASS_NAME, bookmark_button_class_name
        ).click()
        time.sleep(0.5)
        self.assertIn(
            f"film{self.film_id}-bookmark-yellow-tag",
            self.browser.find_element(
                By.CLASS_NAME, bookmark_button_class_name
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_bookmark_review_color_change(self):
        """Test review bookmark button color behavior."""
        # login and go to film detail page
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:film-details", args=(self.film_id,))
        )
        # initial bookmark button color should be grey
        bookmark_button_class_name = f"review{self.review.id}-bookmark-button"
        self.assertIn(
            f"review{self.review.id}-bookmark-text-tag-grey",
            self.browser.find_element(
                By.CLASS_NAME, bookmark_button_class_name
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        # after being clicked bookmark button color should be yellow
        self.browser.find_element(
            By.CLASS_NAME, bookmark_button_class_name
        ).click()
        time.sleep(0.5)
        self.assertIn(
            f"review{self.review.id}-bookmark-text-tag-yellow",
            self.browser.find_element(
                By.CLASS_NAME, bookmark_button_class_name
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_bookmark_fandom_color_change(self):
        """Test fandom bookmark button color behavior."""
        # login and go to fandom page
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:fandom", args=(self.fandom_name,))
        )
        # initially bookmark button color should be grey
        bookmark_button_class_name = (
            f"fandom{self.fandom_name}-bookmark-button"
        )
        self.assertIn(
            f"fandom{self.fandom_name}-bookmarked-text-tag-grey",
            self.browser.find_element(
                By.CLASS_NAME, bookmark_button_class_name
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        # after being clicked bookmark button color should be yellow
        self.browser.find_element(
            By.CLASS_NAME, bookmark_button_class_name
        ).click()
        time.sleep(0.5)
        self.assertIn(
            f"fandom{self.fandom_name}-bookmarked-text-tag-yellow",
            self.browser.find_element(
                By.CLASS_NAME, bookmark_button_class_name
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_profile_bookmark_page(self):
        """A profile bookmark page should show bookmarks correctly."""
        # create bookmark for film, review, fandom
        Bookmark.objects.create(owner=self.user, content_object=self.film)
        Bookmark.objects.create(owner=self.user, content_object=self.fandom)
        Bookmark.objects.create(owner=self.user, content_object=self.review)
        # login and go to profile page
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(self.live_server_url + reverse("wongnung:profile"))
        # select profile bookmark components
        profile_bookmark = list(
            filter(
                lambda elements: elements.text == "Bookmarks",
                self.browser.find_elements(By.TAG_NAME, "span"),
            )
        )
        self.assertIsNotNone(profile_bookmark)
        profile_bookmark[0].click()
        # check film bookmark
        time.sleep(0.5)
        # click Films bookmark radio button
        film_bookmark = list(
            filter(
                lambda elements: elements.text == "Films",
                self.browser.find_elements(By.TAG_NAME, "div"),
            )
        )
        self.assertTrue(film_bookmark)
        self.assertEqual(1, len(film_bookmark))
        film_bookmark[0].click()
        time.sleep(0.5)
        # check if a film exist in profile bookmark
        self.assertTrue(
            self.browser.find_element(By.PARTIAL_LINK_TEXT, self.film.title)
        )
        # check review bookmark
        review_bookmark = list(
            filter(
                lambda elements: elements.text == "Reviews",
                self.browser.find_elements(By.TAG_NAME, "div"),
            )
        )
        self.assertTrue(review_bookmark)
        self.assertEqual(1, len(review_bookmark))
        # click Reviews bookmark radio button
        review_bookmark[0].click()
        time.sleep(0.5)
        # check if a review exist in profile bookmark
        self.assertTrue(
            self.browser.find_element(By.CLASS_NAME, f"review{self.review.id}")
        )
        # check fandom bookmark
        fandom_bookmark = list(
            filter(
                lambda elements: elements.text == "Fandoms",
                self.browser.find_elements(By.TAG_NAME, "div"),
            )
        )
        self.assertTrue(fandom_bookmark)
        self.assertEqual(1, len(fandom_bookmark))
        # click Fandoms bookmark radio button
        fandom_bookmark[0].click()
        time.sleep(0.5)
        # check if a fandom exist in profile bookmark
        self.assertTrue(
            self.browser.find_element(By.PARTIAL_LINK_TEXT, self.fandom.name)
        )
