import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from wongnung.globals import htmx_endpoint_with_auth
from wongnung.models.user_profile import UserProfile

logger = logging.getLogger(__name__)

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


@login_required
def save_profile(request):
    profile: UserProfile = request.user.userprofile
    display_name = request.POST["display_name"]
    color = request.POST["color"][1:]
    profile.display_name = display_name
    profile.color = color
    profile.save()
    logger.info(f"Profile updated for user {request.user.username}. New display name: {display_name}, New color: #{color}")
    return profile_page(request)
