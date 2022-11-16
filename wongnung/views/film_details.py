from django.http import Http404
from django.shortcuts import render

from ..globals import htmx_endpoint
from ..models.film import Film
from ..models.review import Review


def film_details_page(request, filmid):
    """Renders a film details page."""
    context = {"filmid": filmid}
    return render(request, "wongnung/film_details_page.html", context)


@htmx_endpoint
def show_film_component(request, filmid):
    """Renders a film component based on filmid."""
    film = Film.get_film(film_id=filmid)
    if not film:
        raise Http404()
    reviews = Review.objects.filter(film=film).order_by("-pub_date")
    context = {"film": film, "reviews": reviews}
    return render(request, "wongnung/film_component.html", context)
