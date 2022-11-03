from django.shortcuts import get_object_or_404, render

from ..models.fandom import Fandom


def show_fandom(request, id):
    fandom = get_object_or_404(Fandom, pk=id)
    context = {
        "fan_name": fandom.name,
        "mebers_num": fandom.get_member_count()
    }
    return render(request, "wongnung/fandom_page.html", context)
