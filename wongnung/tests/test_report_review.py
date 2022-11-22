import time
from unittest.mock import patch
from selenium import webdriver
from django.test.client import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from wongnung.models.film import Film
from wongnung.models.review import Review
from wongnung.models.report import Report
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .utils import get_response_credits, get_response_info, new_test_user


class ReportReviewTest(StaticLiveServerTestCase):
    """End-to-end tests for reportting review."""

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
        self.username = "demouser1"
        self.password = "demopass123"
        self.user = new_test_user(self.username, self.password)
        self.film_id = "0"
        self.film = Film.get_film(self.film_id)
        self.review = Review.objects.create(
            film=self.film,
            author=self.user,
            content="This is review for report testing",
        )
        self.review_2 = Review.objects.create(
            film=self.film, content="This is review for report testing (2)"
        )
        self.review_3 = Review.objects.create(
            film=self.film, content="This is review for report testing (3)"
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

    def test_cancel_report_review(self):
        """If user click the cancel button report modal will disappear."""
        # login, then go to feed page
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(self.live_server_url + reverse("wongnung:feed"))

        # scroll down the feed untill every review show up.
        feed_id = "feedContinue"
        elements = self.browser.find_elements(By.ID, feed_id)
        for element in elements:
            element.location_once_scrolled_into_view

        # click report button on review component
        review_classname = f"review{self.review_2.id}"
        report_button_classname = f"reportReview{self.review_2.id}"
        self.browser.find_element(
            By.CLASS_NAME, review_classname
        ).find_element(By.CLASS_NAME, report_button_classname).click()
        time.sleep(0.2)
        # find review's report modal
        report_modal_id = f"ReportModal{self.review_2.id}"
        report_modal = self.browser.find_element(By.ID, report_modal_id)
        cancel_button = list(
            filter(
                lambda elements: elements.text == "Cancel",
                report_modal.find_elements(By.TAG_NAME, "button"),
            )
        )
        cancel_button[0].click()
        time.sleep(0.2)
        self.assertIn(
            "hidden",
            self.browser.find_element(By.ID, report_modal_id).get_attribute(
                "class"
            ),
        )

    def test_report_review(self):
        """After user submit review's report, report should save to database."""
        # login, then go to feed page
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(self.live_server_url + reverse("wongnung:feed"))

        # scroll down the feed untill every review show up.
        feed_id = "feedContinue"
        elements = self.browser.find_elements(By.ID, feed_id)
        for element in elements:
            element.location_once_scrolled_into_view

        # click report button on review component
        review_classname = f"review{self.review_2.id}"
        report_button_classname = f"reportReview{self.review_2.id}"
        self.browser.find_element(
            By.CLASS_NAME, review_classname
        ).find_element(By.CLASS_NAME, report_button_classname).click()
        time.sleep(0.1)
        # find review's report modal
        report_modal_id = f"ReportModal{self.review_2.id}"
        report_modal = self.browser.find_element(By.ID, report_modal_id)
        # if user submit report without typing reason, nothing happen.
        submit_button = list(
            filter(
                lambda elements: elements.text == "Report",
                report_modal.find_elements(By.TAG_NAME, "button"),
            )
        )
        submit_button[0].click()
        # input reason to report, then submit it.
        time.sleep(0.1)
        self.browser.find_element(By.ID, report_modal_id).find_element(
            By.TAG_NAME, "textarea"
        ).click()
        self.browser.find_element(By.ID, report_modal_id).find_element(
            By.TAG_NAME, "textarea"
        ).send_keys("Test report")
        submit_button = list(
            filter(
                lambda elements: elements.text == "Report",
                self.browser.find_element(
                    By.ID, report_modal_id
                ).find_elements(By.TAG_NAME, "button"),
            )
        )
        submit_button[0].click()
        # after user submit the report, report modal will disappear.
        self.assertIn(
            "hidden",
            self.browser.find_element(By.ID, report_modal_id).get_attribute(
                "class"
            ),
        )
        self.browser.refresh()
        # after user report the review, it should save to database
        reviews_in_report = [report.review for report in Report.objects.all()]
        self.assertIn(self.review_2, reviews_in_report)
