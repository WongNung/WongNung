from django.shortcuts import render


def error_404_view(request):
    return render(request, "404.html", status=404)
