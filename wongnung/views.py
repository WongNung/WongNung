from typing import Collection, Mapping, Optional

import tmdbsimple as tmdb
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .feed import FeedManager, FeedSession
from .globals import SEARCH_CACHE
from .models import Film, Review

feed_manager = FeedManager()


@login_required
def feed(request: HttpRequest):
    user_id = request.user.pk
    feed_manager.get_feed_session(user_id)
    return render(request, "wongnung/feed.html")


@login_required
def get_feed(request: HttpRequest):
    user_id = request.user.pk
    feed: FeedSession = feed_manager.get_feed_session(user_id)
    try:
        review = feed.pop()
    except TypeError:
        return HttpResponse(
            """<span class="text-center text-white text-xl">The end.</span>"""
        )
    feed.save(feed_manager)
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,)) + "?feed=true"
    )


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
    reviews = Review.objects.filter(film=film)
    context = {"film": film, "reviews": reviews}
    return render(request, "wongnung/film_component.html", context)


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
        "min-w-80",
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


def show_review_component(request: HttpRequest, pk):
    review = Review.objects.get(pk=pk)
    user = request.user
    upvote = review.upvotes.filter(id=user.pk).exists()
    downvote = review.downvotes.filter(id=user.pk).exists()
    context = {
        "review": review,
        "fst_char": review.author.username[0] if review.author else "a",
        "film": review.film,
        "votes": review.get_votes(),
        "upvote": upvote,
        "downvote": downvote,
    }
    if request.GET.get("feed"):
        context["feed"] = "true"
    return render(request, "wongnung/review_component.html", context)


def post_review(request, filmid):
    author = request.user
    film = Film.get_film(filmid)
    content = request.POST["content"].strip()
    print(content)
    if not content:
        return redirect("wongnung:new-review", filmid=filmid)
    review = Review.objects.create(film=film, content=content, author=author)
    return redirect("wongnung:review-component", pk=review.pk)


@login_required
def vote(request, pk):
    """Since votes should now be HTMX requests, we need to use HTMX"""
    review = get_object_or_404(Review, pk=pk)
    user = request.user
    if request.method == "POST":
        if request.POST.get("up"):
            if review.upvotes.filter(id=user.id).exists():
                review.remove_upvotes(request.user)
            else:
                review.add_upvotes(request.user)
                review.remove_downvotes(request.user)
        if request.POST.get("down"):
            if review.downvotes.filter(id=user.id).exists():
                review.remove_downvotes(request.user)
            else:
                review.add_downvotes(request.user)
                review.remove_upvotes(request.user)
    review.save()
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,)),
    )
