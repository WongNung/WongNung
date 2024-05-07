import logging

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)

class CancellableAccountAdapter(DefaultSocialAccountAdapter):
    """
    A Social Account Adapter for allauth, to instead redirect users to
    login page whenever an auth error occurs.
    """

    def authentication_error(
        self,
        request,
        provider_id,
        error=None,
        exception=None,
        extra_context=None,
    ):
        logger.warning(f"Authentication error occurred for provider {provider_id}: {str(error)}")
        raise ImmediateHttpResponse(
            HttpResponseRedirect(reverse("account_login"))
        )
