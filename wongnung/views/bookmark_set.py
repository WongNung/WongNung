from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from wongnung.globals import htmx_endpoint_with_auth
from ..models.film import Film
from ..models.review import Review
from ..models.fandom import Fandom
from wongnung.models.bookmark import get_bookmark_set


@login_required
def show_bookmarks(request):
    return render(request, "wongnung/bookmark_set_page.html")


@htmx_endpoint_with_auth
@login_required
def get_bookmarks_film_set(request):
    user = request.user
    ct = ContentType.objects.get(model='film')
    bookmark_set = get_bookmark_set(ct, user)
    new_set = []
    for bm in bookmark_set:
        new_set += [Film.get_film(bm.object_id)]
    context = {"bookmark_set": new_set}
    return render(request, "wongnung/bookmark_film_set_component.html", context)
