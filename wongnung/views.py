from django.shortcuts import render
from .models import Film, Review


def show_film_component(request, filmid):
    film = Film.get_film(film_id=filmid)
    context = {
        'film': film
    }
    return render(request, 'wongnung/film_component.html', context)

def show_review_component(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        'review': review
    }
    return render(request, 'wongnung/review_componet.html', context)
