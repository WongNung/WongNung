from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..feed import FeedSession
from ..globals import htmx_endpoint_with_auth
from ..models import Review
from . import feed_manager


@login_required
def feed(request: HttpRequest):
    """Renders a feed page."""
    user_id = request.user.pk
    feed_manager.get_feed_session(user_id)
    return render(request, "wongnung/feed.html")


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
    feed.save(feed_manager)
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,)) + "?feed=true"
    )
