from .views import (
    show_film_component,
    show_review_component,
    search,
    film_details_page,
    post_review_page,
    post_review,
    feed,
    vote,
)
from django.urls import path


app_name = "wongnung"
urlpatterns = [
    path("", feed, name="feed"),
    path("film/<str:filmid>", film_details_page, name="film-details"),
    path("new_review/<str:filmid>", post_review_page, name="new-review"),
    path("post_review/<str:filmid>", post_review, name="post-review"),
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
    path("show_review_component/<int:pk>/vote", vote, name="vote"),
]

urlpatterns += htmx_paths
