from django.shortcuts import render


def about_us(request):
    return render(request, "wongnung/about_us.html")
