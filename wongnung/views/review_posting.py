from re import findall
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from wongnung.globals import htmx_endpoint

from ..models.film import Film
from ..models.review import Review


@login_required
def post_review_page(request, filmid):
    """Renders a review posting page."""
    film = Film.get_film(film_id=filmid)
    context = {"film": film}
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

    Review.objects.create(film=film, content=content, author=author)
    return redirect("wongnung:film-details", filmid=filmid)
