from typing import Optional, Mapping, Collection
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .globals import SEARCH_CACHE
from .models import Film, Review
import tmdbsimple as tmdb
from django.contrib.auth.decorators import login_required


def test_page(request):
    return render(request, "wongnung/test_page.html")


def film_details_page(request, filmid):
    context = {"filmid": filmid}
    return render(request, "wongnung/film_details_page.html", context)


@login_required
def post_review_page(request, filmid):
    film = Film.get_film(film_id=filmid)
    context = {"film": film}
    return render(request, "wongnung/post_review_page.html", context)


def show_film_component(request, filmid):
    film = Film.get_film(film_id=filmid)
    context = {"film": film}
    return render(request, "wongnung/film_component.html", context)


def search(request: HttpRequest):
    query = str(request.GET.get("query")).lower()

    if len(query) < 3:
        return HttpResponse(construct_results_container())

    if not SEARCH_CACHE.get(query):
        print("Calling TMDB API")
        search = tmdb.Search()
        res = search.movie(query=query)["results"]
        SEARCH_CACHE.set(query, res, 300) 
    
    results = SEARCH_CACHE.get(query)
    if not results:
        return HttpResponse(construct_results_container())
    if len(results) > 5:
        results = results[:5]

    return HttpResponse(construct_results_container(results))


def construct_results_container(
    search_results: Optional[Collection] = None,
) -> str:
    container_cls = [
        "mx-6",
        "my-4",
        "px-5",
        "py-4",
        "absolute",
        "overflow-x-hidden",
        "max-w-3xl",
        "flex",
        "flex-col",
        "bg-white",
        "rounded-md",
        "shadow-lg",
    ]
    if not search_results or len(search_results) <= 0:
        container_cls += ["hidden"]
        return f'<div class="{" ".join(container_cls)}" id="search-results"></div>'
    entries_html = "\n".join(
        construct_result_entry_span(film) for film in search_results
    )
    return f"""<div class="{" ".join(container_cls)}" id="search-results">
    {entries_html}
    </div>"""


def construct_result_entry_span(film: Mapping) -> str:
    result_cls = [
        "m-1",
        "text-black",
        "hover:text-component-red",
    ]
    text = film["title"]
    if "release_date" in film.keys():
        year = film["release_date"].split("-")[0]
        text = f"{text} ({year})"
    return f"""<span class="{" ".join(result_cls)}">
    <a href="/film/{film["id"]}"
    class="hover:underline">{text}</a>
    </span>"""


def show_review_component(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        "review": review,
        "fst_char": review.author.username[0] if review.author else "a",
        "film": review.film,
    }
    return render(request, "wongnung/review_componet.html", context)


def post_review(request, filmid):
    author = request.user
    film = Film.get_film(filmid)
    content = request.POST["content"].strip()
    print(content)
    if not content:
        return redirect("wongnung:new-review", filmid=filmid)
    review = Review.objects.create(film=film, content=content, author=author)
    return redirect("wongnung:review-component", pk=review.id)
