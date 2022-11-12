from datetime import tzinfo
from urllib import parse

import pytz
from django.http import HttpRequest
from django.utils import timezone

from .models.user_profile import UserProfile


class LocalTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.COOKIES.get("timezone"):
            timezone.activate(
                pytz.timezone(parse.unquote(request.COOKIES.get("timezone")))
            )
        return self.get_response(request)


class EnsureUserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated and not hasattr(
            request.user, "userprofile"
        ):
            UserProfile.objects.create(user=request.user)
        return self.get_response(request)
