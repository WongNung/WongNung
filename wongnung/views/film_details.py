from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from wongnung.globals import htmx_endpoint

from ..models.film import Film
from ..models.review import Review


def film_details_page(request, filmid):
    """Renders a film details page."""
    if not Film.get_film(film_id=filmid):
        return HttpResponseRedirect(reverse("wongnung:feed"))
    context = {"filmid": filmid}
    return render(request, "wongnung/film_details_page.html", context)


@htmx_endpoint
def show_film_component(request, filmid):
    """Renders a film component based on filmid."""
    film = Film.get_film(film_id=filmid)
    reviews = Review.objects.filter(film=film).order_by("-pub_date")
    context = {"film": film, "reviews": reviews}
    return render(request, "wongnung/film_component.html", context)
