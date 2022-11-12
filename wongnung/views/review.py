from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse

from wongnung.globals import htmx_endpoint

from ..models.review import Review
from wongnung.models.bookmark import Bookmark


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

    context = {
        "review": review,
        "fst_char": review.author.username[0] if review.author else "?",
        "film": review.film,
        "votes": review.get_votes(),
        "upvote": upvote,
        "downvote": downvote,
        "bookmark_status": bm,
    }
    if request.GET.get("feed"):
        context["feed"] = "true"
    return render(request, "wongnung/review_component.html", context)
