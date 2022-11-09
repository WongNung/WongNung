from datetime import tzinfo
from urllib import parse

import pytz
from django.http import HttpRequest
from django.utils import timezone


class LocalTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if not request.COOKIES.get("timezone"):
            return self.get_response(request)
        timezone.activate(
            pytz.timezone(parse.unquote(request.COOKIES.get("timezone")))
        )
        return self.get_response(request)
