from django.http import HttpRequest
from django.shortcuts import render

from ..globals import htmx_endpoint
from ..models.review import Review


@htmx_endpoint
def show_review_component(request: HttpRequest, pk):
    """Renders a review component based on primary key."""
    review = Review.objects.get(pk=pk)
    user = request.user
    upvote = review.upvotes.filter(id=user.pk).exists()
    downvote = review.downvotes.filter(id=user.pk).exists()
    context = {
        "review": review,
        "fst_char": review.author.username[0] if review.author else "a",
        "film": review.film,
        "votes": review.get_votes(),
        "upvote": upvote,
        "downvote": downvote,
    }
    if request.GET.get("feed"):
        context["feed"] = "true"
    return render(request, "wongnung/review_component.html", context)
