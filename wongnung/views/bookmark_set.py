from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from wongnung.globals import htmx_endpoint_with_auth
from ..models.review import Review
from django.db.models import Q
from wongnung.models.bookmark import get_bookmark_set


@login_required
def show_bookmarks(request):
    return render(request, "wongnung/bookmark_set_page.html")


@htmx_endpoint_with_auth
@login_required
def get_bookmarks_set(request):
    user = request.user
    ct = ContentType.objects.get(model=request.POST.get("type"))
    bookmark_set = [
        bookmark.content_object for bookmark in get_bookmark_set(ct, user)
    ]
    if ct.name == "fandom":
        fandom_dict = {}
        for fandom in bookmark_set:
            reviews = Review.objects.filter(
                Q(film__genres__icontains=fandom.name)
                | Q(content__icontains=f"#{fandom.name}")
            ).order_by("-pub_date")
            latest = reviews.first()
            last_active = None
            if latest:
                last_active = latest.pub_date
            fandom_dict[fandom] = last_active
        bookmark_set = fandom_dict
    context = {f"{ct.name}_set": bookmark_set}
    return render(request, request.POST.get("template"), context)
