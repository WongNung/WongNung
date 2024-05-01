import logging
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse

from ..globals import htmx_endpoint
from ..models.review import Review
from wongnung.models.bookmark import Bookmark

logger = logging.getLogger(__name__)

def _color_by_bg(color_hex: str) -> str:
    """
    Pick black or white based on bg color
    Ref: https://stackoverflow.com/a/3943023
    """
    r, g, b = tuple(int(color_hex[i : i + 2], 16) for i in (0, 2, 4))
    return "000000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "FFFFFF"


@htmx_endpoint
def show_review_component(request: HttpRequest, pk):
    """Renders a review component based on primary key."""
    review = Review.objects.get(pk=pk)
    user = request.user
    upvote = review.upvotes.filter(id=user.pk).exists()
    downvote = review.downvotes.filter(id=user.pk).exists()

    # Try getting Bookmark status
    try:
        user = request.user
        bm = Bookmark.objects.filter(
            content_type=ContentType.objects.get(model="review"),
            owner=user,
            object_id=pk,
        ).exists()
    except (User.DoesNotExist, TypeError):
        bm = False

    if review.author:
        display_name = review.author.userprofile.display_name
        if not display_name:
            display_name = review.author.username
    else:
        display_name = "Anonymous"

    context = {
        "review": review,
        "display_name": display_name,
        "fst_char": display_name[0] if review.author else "?",
        "bgcolor": f"#{review.author.userprofile.color}"
        if review.author
        else "D9D9D9",
        "fgcolor": f"#{_color_by_bg(review.author.userprofile.color)}"
        if review.author
        else "000000",
        "film": review.film,
        "votes": review.get_votes(),
        "upvote": upvote,
        "downvote": downvote,
        "bookmark_status": bm,
    }
    if request.GET.get("feed"):
        context["feed"] = "true"
    return render(request, "wongnung/review_component.html", context)
