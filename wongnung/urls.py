from .views import (
    show_film_component,
    show_review_component,
    test_page,
    search,
    film_details_page,
)
from django.urls import path


app_name = "wongnung"
urlpatterns = [
    path("test", test_page, name="test"),
    path("film/<str:filmid>", film_details_page, name="film-details"),
]

# Use this array to store paths that should be called using htmx
htmx_paths = [
    path(
        "show_film_component/<str:filmid>",
        show_film_component,
        name="film-component",
    ),
    path(
        "show_review_component/<int:pk>",
        show_review_component,
        name="review-component",
    ),
    path("search", search, name="search"),
]

urlpatterns += htmx_paths
