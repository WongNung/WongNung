from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from .models import Film, Review, Report
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
                    <a href="/film/{film["id"]}"
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
        "shadow-lg",
        f"{'' if len(query) >= 3 and results_html else 'hidden'}",
    ]

    html = f'<div class="{" ".join(container_cls)}" id="search-results">'
    html += results_html
    html += "</div>"
    return HttpResponse(html)


def show_review_component(request, pk):
    review = Review.objects.get(pk=pk)
    user = request.user
    upvote = review.upvotes.filter(id=user.id).exists()
    downvote = review.downvotes.filter(id=user.id).exists()
    context = {
        "review": review,
        "fst_char": review.author.username[0] if review.author else "a",
        "film": review.film,
        "votes": review.get_votes(),
        "upvote": upvote,
        "downvote": downvote
    }
    return render(request, "wongnung/review_component.html", context)


def post_review(request, filmid):
    author = request.user
    film = Film.get_film(filmid)
    content = request.POST["content"].strip()
    if not content:
        return redirect("wongnung:new-review", filmid=filmid)
    review = Review.objects.create(film=film, content=content, author=author)
    return redirect("wongnung:review-component", pk=review.id)


@login_required
def vote(request, pk):
    review = get_object_or_404(Review, pk=pk)
    user = request.user
    if request.method == "POST":
        if request.POST.get('up'):
            if review.upvotes.filter(id=user.id).exists():
                review.remove_upvotes(request.user)
            else:
                review.add_upvotes(request.user)
                review.remove_downvotes(request.user)
        if request.POST.get('down'):
            if review.downvotes.filter(id=user.id).exists():
                review.remove_downvotes(request.user)
            else:
                review.add_downvotes(request.user)
                review.remove_upvotes(request.user)
    review.save()
    return HttpResponseRedirect(reverse('wongnung:review-component', args=(review.id,)))


@login_required
def report(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect("wongnung:report-modal-cancel", pk=pk, )
        content = request.POST["report-content"].strip()
        if not content:
            return redirect("wongnung:report-modal", pk=pk)
        report = Report.objects.create(
            review=review, user=request.user, content=content)
        report.save()
    return HttpResponseRedirect(reverse('wongnung:review-component', args=(review.id,)))


@login_required
def show_report_modal(request, pk, cancel=""):
    review = get_object_or_404(Review, pk=pk)
    context = {"review" : review}
    if cancel:
        context["cancel"] = True
    return render(request, "wongnung/report_modal_component.html", context)
