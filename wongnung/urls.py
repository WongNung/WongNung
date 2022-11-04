from django.urls import path

# fmt: off
from .views.feed import feed, get_feed
from .views.film_details import film_details_page, show_film_component
from .views.review import show_review_component
from .views.review_posting import post_review, post_review_page
from .views.review_reporting import report, show_report_modal
from .views.review_voting import vote
from .views.search import cancel_search, search
from .views.fandom import show_fandom, join_fandom, leave_fandom

# fmt: on

app_name = "wongnung"
urlpatterns = [
    path("", feed, name="feed"),
    path("film/<str:filmid>", film_details_page, name="film-details"),
    path("new_review/<str:filmid>", post_review_page, name="new-review"),
    path("post_review/<str:filmid>", post_review, name="post-review"),
    path("fandom/<int:id>", show_fandom, name="fandom"),
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
    path("show_review_component/<int:pk>/vote", vote, name="vote"),
    path("show_review_component/<int:pk>/report", report, name="report"),
    path("show_report_modal/<int:pk>", show_report_modal, name="report-modal"),
    path(
        "show_report_modal/<int:pk>/cancel",
        show_report_modal,
        {"cancel": "true"},
        name="report-modal-cancel",
    ),
    path("search", search, name="search"),
    path("cancel_search", cancel_search, name="cancel-search"),
    path("get_feed", get_feed, name="get-feed"),
    path("fandom/<int:id>/join", join_fandom, name="join-fandom"),
    path("fandom/<int:id>/leave", leave_fandom, name="leave-fandom"),
]

urlpatterns += htmx_paths
