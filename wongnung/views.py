from django.shortcuts import render
from .models import Film


def show_film_component(request, filmid):
    film = Film.get_film(film_id=filmid)
    context = {
        'film': film
    }
    return render(request, 'wongnung/film_component.html', context)
