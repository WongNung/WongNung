from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models.fandom import Fandom


def show_fandom(request, id):
    fandom = get_object_or_404(Fandom, pk=id)
    if request.user in fandom.get_all_member():
        status = True
    context = {
        "fandom": fandom,
        "members_num": fandom.get_member_count(),
        "last_active": "1 hr",
        "status": status
    }
    return render(request, "wongnung/fandom_page.html", context)

@login_required
def join_fandom(request, id):
    fandom = get_object_or_404(Fandom, id=id)
    user = request.user
    fandom.add_member(user)
    fandom.save()
    return HttpResponseRedirect(reverse("wongnung:fandom", args=(fandom.id,)))
