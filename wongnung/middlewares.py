import logging
from urllib import parse

import pytz
from django.http import HttpRequest
from django.utils import timezone

from .models.user_profile import UserProfile

logger = logging.getLogger(__name__)

class LocalTimeMiddleware:
    """A middleware that will apply a user's timezone based on their cookies, whenever a user navigates to anywhere in the site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.COOKIES.get("timezone"):
            try:
                timezone.activate(pytz.timezone(parse.unquote(request.COOKIES.get("timezone"))))
            except pytz.UnknownTimeZoneError as e:
                logger.warning(f"Unknown timezone in cookie: {str(e)}")
        else:
            logger.info("No timezone cookie found, using default timezone.")

        return self.get_response(request)


class EnsureUserProfileMiddleware:
    """A middleware that ensures the user their own UserProfile."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated and not hasattr(
            request.user, "userprofile"
        ):
            try:
                UserProfile.objects.create(user=request.user)
                logger.info(f"Created UserProfile for user {request.user.id}.")
            except Exception as e:
                logger.error(f"Error creating UserProfile for user {request.user.id}: {str(e)}")

        return self.get_response(request)
