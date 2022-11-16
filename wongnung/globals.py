from functools import wraps

from django.core.cache import caches
from django.http import HttpResponseForbidden
from django_htmx.http import HttpResponseClientRedirect

SEARCH_CACHE = caches["searches"]  # Cache for search results


def htmx_endpoint(function, required_auth=False):
    """
    A decorator function that requires requests sent to
    be from HTMX. Any requests that are not from HTMX will be
    raised with Forbidden (403).
    """

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.htmx:
            if required_auth and (not request.user.is_authenticated):
                return HttpResponseClientRedirect("/accounts/login")
            return function(request, *args, **kwargs)
        return HttpResponseForbidden("Explicit backend calls not allowed!")

    return wrap


def htmx_endpoint_with_auth(function):
    """Requires request sent to be from HTMX and authenticated user."""
    return htmx_endpoint(function, required_auth=True)
