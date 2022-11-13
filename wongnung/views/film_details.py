from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from wongnung.globals import htmx_endpoint
from wongnung.insights import UserSeesFilm
from . import user_insights
from ..models.film import Film
from ..models.review import Review
from wongnung.models.bookmark import Bookmark, get_bookmark_set


def film_details_page(request, filmid):
    """Renders a film details page."""
    context = {"filmid": filmid}
    return render(request, "wongnung/film_details_page.html", context)


@htmx_endpoint
def show_film_component(request, filmid):
    """Renders a film component based on filmid."""
    try:
        bm = Bookmark.objects.filter(
            content_type=ContentType.objects.get(model="film"),
            owner=request.user,
            object_id=str(filmid),
        ).exists()
    except (User.DoesNotExist, TypeError):
        bm = False
    film = Film.get_film(film_id=filmid)
    reviews = Review.objects.filter(film=film).order_by("-pub_date")
    if request.user.is_authenticated:
        user_insights.push(request.user, UserSeesFilm(film))
    context = {"film": film, "reviews": reviews, "bookmark_status": bm}
    return render(request, "wongnung/film_component.html", context)
