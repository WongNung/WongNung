from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from wongnung.globals import htmx_endpoint_with_auth
from wongnung.models.bookmark import (
    Bookmark,
    get_bookmark_set,
    delete_bookmark,
)
from wongnung.models.film import Film
from wongnung.models.fandom import Fandom
from wongnung.models.review import Review

@htmx_endpoint_with_auth
@login_required
def add_bookmark_view(request):
    user = request.user
    bookmark_id = request.POST["bookmark"]
    url = request.POST["url"]
    ct_type = request.POST["type"]
    if ct_type == "film":
        Bookmark.objects.create(
            owner=user, content_object=Film.get_film(bookmark_id)
        )
    elif ct_type == "fandom":
        Bookmark.objects.create(
            owner=user, content_object=Fandom.objects.get(name=bookmark_id)
        )
    elif ct_type == "review":
        Bookmark.objects.create(
            owner=user, content_object=Review.objects.get(pk=bookmark_id)
        )
    return HttpResponseRedirect(reverse(url, args=(bookmark_id,)))

@htmx_endpoint_with_auth
@login_required
def delete_bookmark_view(request):
    user = request.user
    bookmark_id = request.POST["bookmark"]
    url = request.POST["url"]
    ct_type = request.POST["type"]
    ct = ContentType.objects.get(model=ct_type)
    delete_bookmark(ct, user, bookmark_id)
    return HttpResponseRedirect(reverse(url, args=(bookmark_id,)))
