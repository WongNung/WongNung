import logging
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from ..feed import FeedSession
from ..globals import htmx_endpoint_with_auth
from ..models import Review
from . import feed_manager

logger = logging.getLogger(__name__)

def feed(request: HttpRequest):
    """Renders a feed page."""
    if not request.user.is_authenticated:
        logger.warning("Unauthenticated user tried to access the feed.")
        return redirect(reverse("wongnung:landing"))
    user_id = request.user.pk
    
    try:
        feed_manager.get_feed_session(user_id)
    except Exception as e:
        logger.error(f"Error getting feed session for user {user_id}: {str(e)}")

    logger.info(f"Rendering feed for user {user_id}.")
    return render(
        request,
        "wongnung/feed.html",
        {
            "user": request.user,
            "profile": request.user.userprofile
            if request.user.is_authenticated
            else None,
        },
    )


@htmx_endpoint_with_auth
@login_required
def get_feed(request):
    """Retrieves and renders feed component from feed session."""
    user_id = request.user.pk
    feed: FeedSession = feed_manager.get_feed_session(user_id, renew=False)
    review: Optional[Review] = feed.pop()
    if not review:
        return HttpResponse(
            """<span class="text-center text-white text-xl">The end.</span>"""
        )
    try:
        feed.save(feed_manager)
    except Exception as e:
        logger.error(f"Error saving feed session for user {user_id}: {str(e)}")
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,)) + "?feed=true"
    )
