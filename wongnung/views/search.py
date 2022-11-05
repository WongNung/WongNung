from typing import Collection, Mapping, Optional

import tmdbsimple as tmdb
from django.http import HttpRequest, HttpResponse

from ..globals import SEARCH_CACHE, htmx_endpoint


@htmx_endpoint
def search(request: HttpRequest):
    query = str(request.GET.get("query")).lower()

    if len(query) < 3:
        return HttpResponse(construct_results_container())

    if not SEARCH_CACHE.get(query):
        search = tmdb.Search()
        res = search.movie(query=query)["results"]
        SEARCH_CACHE.set(query, res, 300)

    results = SEARCH_CACHE.get(query)
    if not results:
        return HttpResponse(construct_results_container())

    return HttpResponse(construct_results_container(results))


@htmx_endpoint
def cancel_search(request: HttpRequest):
    return HttpResponse(construct_results_container())


def construct_results_container(
    search_results: Optional[Collection] = None,
) -> str:
    container_cls = [
        "mx-6",
        "my-4",
        "px-5",
        "py-4",
        "absolute",
        "overflow-x-clip",
        "overflow-y-auto",
        "max-w-80",
        "max-h-80",
        "flex",
        "flex-col",
        "bg-white",
        "rounded-md",
        "shadow-lg",
        "z-10",
        "scrollbar",
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
