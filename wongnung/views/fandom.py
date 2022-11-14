import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from wongnung.models.review import Review

from ..models.fandom import Fandom
from wongnung.models.bookmark import Bookmark


def get_fandom(name: str) -> Fandom:
    """Gets a fandom object from the name, if doesn't exist, raise 404."""
    name = re.sub(r"\s+", "", name.strip(), flags=re.UNICODE)
    try:
        return Fandom.objects.get(name__iexact=name)
    except Fandom.DoesNotExist:
        return Fandom.objects.create(name=name)


def fandom_page(request, name):
    fandom = get_fandom(name)
    context = {
        "fandom": fandom,
        "user": request.user,
        "profile": request.user.userprofile
        if request.user.is_authenticated
        else None,
    }
    return render(request, "wongnung/fandom_page.html", context)


def show_fandom(request, name):
    """Renders a fandom page according to name given."""
    fandom = get_fandom(name)
    user_status = request.user in fandom.get_all_member()

    try:
        bm = Bookmark.objects.filter(
            content_type=ContentType.objects.get(model="fandom"),
            owner=request.user,
            object_id=name,
        ).exists()
    except (User.DoesNotExist, TypeError):
        bm = False

    reviews = Review.objects.filter(
        Q(film__genres__icontains=fandom.name)
        | Q(content__icontains=f"#{fandom.name}")
    ).order_by("-pub_date")

    latest = reviews.first()
    last_active = None
    if latest:
        last_active = latest.pub_date

    context = {
        "fandom": fandom,
        "members_num": fandom.get_member_count(),
        "last_active": last_active,
        "user_status": user_status,
        "reviews": reviews,
        "bookmark_status": bm,
    }
    return render(request, "wongnung/fandom_component.html", context)


@login_required
def join_fandom(request, name):
    """User joins a fandom via this endpoint."""
    fandom = get_fandom(name)
    user = request.user
    fandom.add_member(user)
    fandom.save()
    return HttpResponseRedirect(reverse("wongnung:fandom", args=(fandom.pk,)))


@login_required
def leave_fandom(request, name):
    """User leaves a fandom via this endpoint."""
    fandom = get_fandom(name)
    user = request.user
    fandom.remove_member(user)
    fandom.save()
    return HttpResponseRedirect(reverse("wongnung:fandom", args=(fandom.pk,)))
