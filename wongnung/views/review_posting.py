import logging
from re import findall
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..globals import htmx_endpoint
from ..insights import UserWritesReview

from ..models.film import Film
from ..models.review import Review
from . import user_insights

logger = logging.getLogger(__name__)

@login_required
def post_review_page(request, filmid):
    """Renders a review posting page."""
    film = Film.get_film(film_id=filmid)
    context = {
        "film": film,
        "user": request.user,
        "profile": request.user.userprofile,
    }
    review = Review.objects.filter(film=film, author=request.user).first()
    if review:
        context["review"] = review
    return render(request, "wongnung/post_review_page.html", context)


def post_review(request, filmid):
    """An endpoint for saving a new review."""
    author = request.user
    film = Film.get_film(filmid)
    content = request.POST["content"].strip()
    if not content:
        return redirect("wongnung:new-review", filmid=filmid)

    # Quick-and-dirty sanitization
    for tag in findall(r"<{1}.+>{1}", content):
        content = content.replace(tag, "")

    review = Review.objects.filter(film=film, author=author).first()
    if review:
        review.content = content
        review.save()
        logger.info(f"Updated review with id {review.id} for film {filmid} by user {request.user.username}.")
    else:
        review = Review.objects.create(
            film=film, content=content, author=author
        )
        logger.info(f"Created review with id {review.id} for film {filmid} by user {request.user.username}.")
    user_insights.push(author, UserWritesReview(film, review))
    return redirect("wongnung:film-details", filmid=filmid)
