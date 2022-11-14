from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from wongnung.globals import htmx_endpoint_with_auth
from ..models.film import Film
from ..models.review import Review
from ..models.fandom import Fandom
from django.db.models import Q
from wongnung.models.bookmark import get_bookmark_set


@login_required
def show_bookmarks(request):
    return render(request, "wongnung/bookmark_set_page.html")


@htmx_endpoint_with_auth
@login_required
def get_bookmarks_film_set(request):
    user = request.user
    ct = ContentType.objects.get(model='film')
    film_bookmark_set = [
        bookmark.content_object for bookmark in get_bookmark_set(ct, user)]
    context = {"bookmark_set": film_bookmark_set}
    return render(request, "wongnung/bookmark_film_set_component.html", context)


@htmx_endpoint_with_auth
@login_required
def get_bookmarks_review_set(request):
    user = request.user
    ct = ContentType.objects.get(model='review')
    review_bookmark_set = [
        bookmark.content_object for bookmark in get_bookmark_set(ct, user)]
    context = {"review_set": review_bookmark_set}
    return render(request, "wongnung/bookmark_review_set_component.html", context)


@htmx_endpoint_with_auth
@login_required
def get_bookmarks_fandom_set(request):
    user = request.user
    ct = ContentType.objects.get(model='fandom')
    fandom_bookmark_set = [
        bookmark.content_object for bookmark in get_bookmark_set(ct, user)]
    fandom_dict = {}
    for fandom in fandom_bookmark_set:
        reviews = Review.objects.filter(
            Q(film__genres__icontains=fandom.name)
            | Q(content__icontains=f"#{fandom.name}")
        ).order_by("-pub_date")
        latest = reviews.first()
        last_active = None
        if latest:
            last_active = latest.pub_date
        fandom_dict[fandom] = last_active

    context = {"fandom_set": fandom_dict}
    return render(request, "wongnung/bookmark_fandom_set_component.html", context)
