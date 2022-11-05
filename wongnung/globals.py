from functools import wraps

from django.core.cache import caches
from django.http import HttpResponseForbidden
from django_htmx.http import HttpResponseClientRedirect

SEARCH_CACHE = caches["searches"]


def htmx_endpoint(function, required_auth=False):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.htmx:
            if required_auth and (not request.user.is_authenticated):
                return HttpResponseClientRedirect("/accounts/login")
            return function(request, *args, **kwargs)
        return HttpResponseForbidden("Explicit backend calls not allowed!")

    return wrap


htmx_endpoint_with_auth = lambda func: htmx_endpoint(func, required_auth=True)
