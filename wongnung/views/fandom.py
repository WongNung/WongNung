import re

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..models.fandom import Fandom
from ..models.review import Review


def get_fandom(name: str) -> Fandom:
    """Gets a fandom object from the name, if doesn't exist, raise 404."""
    name = re.sub(r"\s+", "", name.strip(), flags=re.UNICODE)
    try:
        return Fandom.objects.get(name__iexact=name)
    except Fandom.DoesNotExist:
        raise Http404()


def show_fandom(request, name):
    """Renders a fandom page according to name given."""
    fandom = get_fandom(name)
    if request.user in fandom.get_all_member():
        user_status = True
    else:
        user_status = False
    reviews = Review.objects.filter(
        content__icontains=f"#{fandom.name}"
    ).order_by("-pub_date")
    context = {
        "fandom": fandom,
        "members_num": fandom.get_member_count(),
        "last_active": "1 hr",
        "user_status": user_status,
        "reviews": reviews,
    }
    return render(request, "wongnung/fandom_page.html", context)


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
