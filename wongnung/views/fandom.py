import re
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from ..insights import UserJoinsFandom

from ..models.review import Review

from ..models.fandom import Fandom
from . import user_insights
from ..models.bookmark import Bookmark

logger = logging.getLogger(__name__)

def get_fandom(name: str) -> Fandom:
    """Gets a fandom object from the name, if doesn't exist, create a new one."""
    name = re.sub(r"\s+", "", name.strip(), flags=re.UNICODE)
    if len(name) > 64 or not re.match(r"^[a-zA-Z]{1}[a-zA-Z0-9_]+$", name):
        raise Http404()
    try:
        return Fandom.objects.get(name__iexact=name)
    except Fandom.DoesNotExist:
        logger.info(f"Created a fandom {name}")
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

    reviews = [
        review
        for review in
        Review.objects.all().order_by("-pub_date")
        if fandom.name.lower() in review.get_tags()
    ]

    last_active = None
    if reviews:
        last_active = reviews[0].pub_date

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
    user_insights.push(user, UserJoinsFandom(fandom))

    logger.info(f"User {user.username} joined fandom {name}.")
    return HttpResponseRedirect(reverse("wongnung:fandom", args=(fandom.pk,)))


@login_required
def leave_fandom(request, name):
    """User leaves a fandom via this endpoint."""
    fandom = get_fandom(name)
    user = request.user
    fandom.remove_member(user)
    fandom.save()

    logger.info(f"User {user.username} left fandom {name}.")
    return HttpResponseRedirect(reverse("wongnung:fandom", args=(fandom.pk,)))
