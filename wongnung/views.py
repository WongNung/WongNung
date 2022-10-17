from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Film
import tmdbsimple as tmdb


def test_page(request):
    return render(request, "wongnung/test_page.html")


def show_film_component(request, filmid):
    film = Film.get_film(film_id=filmid)
    context = {"film": film}
    return render(request, "wongnung/film_component.html", context)


def search(request: HttpRequest):
    query = request.GET.get("query")

    result_cls = [
        "m-1",
        "text-black",
        "hover:text-component-red",
    ]

    results_html = ""
    if len(query) >= 3:
        search = tmdb.Search()
        res = search.movie(query=query)["results"]
        if res:
            if len(res) > 5:
                res = res[:5]
            for film in res:
                year = film["release_date"].split("-")[0]
                if year:
                    results_html += f"""<span class="{" ".join(result_cls)}">
                    <a href="/show_film_component/{film["id"]}"
                    class="hover:underline">{film["title"]} ({year})</a>
                    </span>"""

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
        "drop-shadow-lg",
        f"{'' if len(query) >= 3 and results_html else 'hidden'}",
    ]

    html = f'<div class="{" ".join(container_cls)}" id="search-results">'
    html += results_html
    html += "</div>"
    return HttpResponse(html)
