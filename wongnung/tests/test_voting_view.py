from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from ..models.film import Film
from ..models.user_profile import UserProfile
from ..models.review import Review
from .utils import get_response_credits, get_response_info, new_test_user

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import time


class TestVotingView(TestCase):
    """Tests for Voting view"""

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.client = Client()
        self.username = "Test"
        self.password = "1234"
        self.user = new_test_user(self.username, self.password)
        self.film = Film.get_film("0")
        self.review = Review.objects.create(
            film=self.film, content="", author=self.user
        )
        self.client.login(username=self.username, password=self.password)

    def test_vote_redirects(self):
        """Voting will refresh the review component"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        resp = self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertRedirects(
            resp, reverse("wongnung:review-component", args=(self.review.pk,))
        )

    def test_upvote_once(self):
        """Upvoting once should only add 1 to upvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 1)
        self.assertEqual(self.review.get_downvotes(), 0)

    def test_downvote_once(self):
        """Downvoting once should only add 1 to downvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 1)

    def test_upvote_twice(self):
        """Upvoting twice should remove existing upvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 0)

    def test_downvote_twice(self):
        """Downvoting twice should remove existing downvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 0)

    def test_alternate_vote(self):
        """Once upvoted, then downvote it should remove the upvote"""
        url = reverse("wongnung:vote", args=(self.review.pk,))
        self.client.post(url, {"up": "up"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 1)
        self.assertEqual(self.review.get_downvotes(), 0)
        self.client.post(url, {"down": "down"}, HTTP_HX_Request="true")
        self.assertEqual(self.review.get_upvotes(), 0)
        self.assertEqual(self.review.get_downvotes(), 1)


class TestVotingE2E(StaticLiveServerTestCase):
    """End-to-end tests for Voting view"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = ChromeOptions()
        options.add_argument("--headless")
        cls.browser = Chrome(options=options)
        cls.browser.implicitly_wait(30)
        cls.browser.set_page_load_timeout(30)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        # create user
        self.client = Client()
        self.username1 = "Tester1"
        self.password1 = "1234"
        self.user1 = new_test_user(self.username1, self.password1)
        UserProfile.objects.create(user=self.user1)

        self.username2 = "Tester2"
        self.password2 = "5678"
        self.user2 = new_test_user(self.username2, self.password2)
        UserProfile.objects.create(user=self.user2)

        # create review for testing
        self.film = Film.get_film("0")
        self.review_1 = Review.objects.create(
            film=self.film, content="Review Number1", author=self.user1
        )
        self.review_2 = Review.objects.create(
            film=self.film, content="Review Number2", author=self.user2
        )

    def login(self):
        self.client.login(username=self.username1, password=self.password1)
        self.client.login(username=self.username2, password=self.password2)
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

    def access_wongnung(self):
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(
            self.live_server_url
            + reverse("wongnung:film-details", args=("0",))
        )

    def scroll_down(self):
        review_1_div = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}"
        )
        self.browser.execute_script(
            "arguments[0].scrollIntoView();", review_1_div
        )

    def test_initial_upvote_downvote_button(self):
        """The color of initial upvote and downvote button should be grey."""
        self.access_wongnung()
        self.scroll_down()

        time.sleep(1)

        # test upvote button
        self.assertIn(
            "text-post-grey",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_2.id}-upvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        self.assertIn(
            "text-post-grey",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_1.id}-upvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

        # test downvote button
        self.assertIn(
            "text-post-grey",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_2.id}-downvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )
        self.assertIn(
            "text-post-grey",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_1.id}-downvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_voted_upvote_downvote_button(self):
        """When clicked upvote or downvote button, the color should change to red."""
        self.access_wongnung()
        self.scroll_down()

        time.sleep(1)

        # test upvote button
        upvote_button1 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-upvote-button"
        )
        upvote_button1.click()
        time.sleep(1)
        self.assertIn(
            "text-component-red",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_2.id}-upvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

        upvote_button2 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-upvote-button"
        )
        upvote_button2.click()
        time.sleep(1)
        self.assertIn(
            "text-component-red",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_1.id}-upvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

        # test downvote button
        downvote_button1 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-downvote-button"
        )
        downvote_button1.click()
        time.sleep(1)
        self.assertIn(
            "text-component-red",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_2.id}-downvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

        downvote_button2 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-downvote-button"
        )
        downvote_button2.click()
        time.sleep(1)
        self.assertIn(
            "text-component-red",
            self.browser.find_element(
                By.CLASS_NAME, f"review{self.review_1.id}-downvote-button"
            )
            .find_element(By.TAG_NAME, "div")
            .get_attribute("class"),
        )

    def test_upvote_num_of_votes(self):
        """When clicking upvote button the number of votes should increase by 1."""
        self.access_wongnung()
        self.scroll_down()

        time.sleep(1)

        # test upvote button
        button1 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-upvote-button"
        )
        button1.click()
        time.sleep(1)
        votes_num1 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-votes"
        ).text
        self.assertEqual("1", votes_num1)

        button2 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-upvote-button"
        )
        button2.click()
        time.sleep(1)
        votes_num2 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-votes"
        ).text
        self.assertEqual("1", votes_num2)

    def test_downvote_num_of_votes(self):
        """When clicking downvote button the number of votes should decrease by 1."""
        self.access_wongnung()
        self.scroll_down()

        time.sleep(1)

        # test downvote button
        button1 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-downvote-button"
        )
        button1.click()
        time.sleep(1)
        votes_num = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-votes"
        ).text
        self.assertEqual("-1", votes_num)

        button2 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-downvote-button"
        )
        button2.click()
        time.sleep(1)
        votes_num = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-votes"
        ).text
        self.assertEqual("-1", votes_num)

    def test_num_of_votes_click_both(self):
        """When click both upvote and downvote the votes number should be zero."""
        self.access_wongnung()
        self.scroll_down()

        button1 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-upvote-button"
        )
        button2 = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_2.id}-downvote-button"
        )
        button1.click()
        button2.click()
        time.sleep(2)
        votes_num = self.browser.find_element(
            By.CLASS_NAME, f"review{self.review_1.id}-votes"
        ).text
        self.assertEqual("0", votes_num)
