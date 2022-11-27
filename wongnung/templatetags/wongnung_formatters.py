from re import findall
from django.urls import reverse
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

TAILWIND_FANDOM_LINK = ["text-component-red", "hover:underline"]


@register.filter(is_safe=True)
def format_fandom_tags(value):
    """Format the entire content that has Fandom tags with hyperlinks"""
    regex = r"#{1}[a-zA-Z]{1}[a-zA-Z0-9_]{1,63}"
    tags = findall(regex, value)
    if not tags:
        return value
    htmlstr = value
    for tag in tags:
        url = reverse("wongnung:fandom", args=(tag[1:],))
        htmlstr = htmlstr.replace(
            tag,
            f'<a class="{" ".join(TAILWIND_FANDOM_LINK)}" href="{url}">{tag}</a>',
        )
    return mark_safe(htmlstr)
