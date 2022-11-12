from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from wongnung.globals import htmx_endpoint_with_auth


@login_required
def profile_page(request):
    """View for Profile page"""
    return render(
        request,
        "wongnung/profile_page.html",
        {"user": request.user, "profile": request.user.userprofile},
    )


@htmx_endpoint_with_auth
@login_required
def profile_settings_component(request):
    return render(
        request,
        "wongnung/profile_settings_component.html",
        {"user": request.user, "profile": request.user.userprofile},
    )
