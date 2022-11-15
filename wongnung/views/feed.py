from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from wongnung.globals import htmx_endpoint_with_auth

from ..feed import FeedSession
from . import feed_manager


def feed(request: HttpRequest):
    """Renders a feed page."""
    if not request.user.is_authenticated:
        return redirect(reverse("wongnung:landing"))
    user_id = request.user.pk
    feed_manager.get_feed_session(user_id)
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
    review = feed.pop()
    if not review:
        return HttpResponse(
            """<span class="text-center text-white text-xl">The end.</span>"""
        )
    feed.save(feed_manager)
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,)) + "?feed=true"
    )
