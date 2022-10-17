from .views import show_film_component, test_page, search
from django.urls import path

app_name = "wongnung"
urlpatterns = [
    path("test", test_page, name="test"),
    path(
        "show_film_component/<str:filmid>",
        show_film_component,
        name="film-component",
    ),
    path("search", search, name="search"),
]
