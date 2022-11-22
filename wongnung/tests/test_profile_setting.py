import time
from unittest.mock import patch
from selenium import webdriver
from django.test.client import Client
from selenium.webdriver.common.by import By
from wongnung.models.user_profile import UserProfile
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .utils import get_response_credits, get_response_info, new_test_user


class ProfileSttingTest(StaticLiveServerTestCase):
    """End-to-end tests for profile setting"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.browser = webdriver.Chrome(options=options)
        cls.browser.implicitly_wait(3)
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

    def test_set_profil(self):
        # login and go to profile page.
        self.browser.get(self.live_server_url)
        self.login()
        self.browser.get(self.live_server_url + reverse("wongnung:profile"))

        # select profile setting tab
        profile_setting_tab = list(
            filter(
                lambda elements: elements.text == "Profile Settings",
                self.browser.find_elements(By.TAG_NAME, "span"),
            )
        )
        self.assertIsNotNone(profile_setting_tab)
        profile_setting_tab[0].click()
        time.sleep(0.2)

        # default display name should be blank ("")
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual("", user_profile.display_name)
        # default display color should be #D9D9D9
        self.assertEqual("D9D9D9", user_profile.color)

        # insert new display name
        self.browser.find_element(By.CLASS_NAME, "displayName").send_keys("Test1234")
        # insert new display color
        self.browser.find_element(By.CLASS_NAME, "profileColor").send_keys("#ff0000")
        # save the change
        self.browser.find_element(By.CLASS_NAME, "saveProfileButton").click()
        time.sleep(0.2)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual("Test1234", user_profile.display_name)
        self.assertEqual("ff0000", user_profile.color)
