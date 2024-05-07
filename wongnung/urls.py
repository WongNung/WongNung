from django.urls import path


# fmt: off
from .views.fandom import join_fandom, leave_fandom, show_fandom, fandom_page
from .views.feed import feed, get_feed
from .views.film_details import film_details_page, show_film_component
from .views.review import show_review_component
from .views.review_posting import post_review, post_review_page
from .views.review_reporting import report, set_report_modal_state
from .views.review_voting import vote
from .views.search import cancel_search, search
from .views.bookmark import add_bookmark_view, delete_bookmark_view
from .views.landing import show_landing_page
from .views.bookmark_set import show_bookmarks, get_bookmarks_set
from .views.about_us import about_us
from .views.privacy_policy import privacy_policy_confirm
from wongnung.views.profile import (
    profile_page,
    profile_settings_component,
    save_profile,
)
from .views.error_handler import error_404_view

# fmt: on

app_name = "wongnung"
urlpatterns = [
    path("", feed, name="feed"),
    path("film/<str:filmid>", film_details_page, name="film-details"),
    path("new_review/<str:filmid>", post_review_page, name="new-review"),
    path("post_review/<str:filmid>", post_review, name="post-review"),
    path("fandom/<name>", fandom_page, name="fandom"),
    path("landing", show_landing_page, name="landing"),
    path("profile", profile_page, name="profile"),
    path("save_profile", save_profile, name="save-profile"),
    path("bookmarks", show_bookmarks, name="bookmarks"),
    path("not_found", error_404_view, name="404"),
    path("privacy_policy", privacy_policy_confirm, name="privacy-policy"),
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
    path("post_review/<str:filmid>", post_review, name="post-review"),
    path("show_review_component/<int:pk>/vote", vote, name="vote"),
    path("show_review_component/<int:pk>/report", report, name="report"),
    path(
        "report_modal/<int:pk>",
        set_report_modal_state,
        name="report-modal",
    ),
    path("search", search, name="search"),
    path("cancel_search", cancel_search, name="cancel-search"),
    path("get_feed", get_feed, name="get-feed"),
    path("fandom/<name>/show", show_fandom, name="show-fandom"),
    path("fandom/<name>/join", join_fandom, name="join-fandom"),
    path("fandom/<name>/leave", leave_fandom, name="leave-fandom"),
    path("add_to_bookmark", add_bookmark_view, name="add-bookmark"),
    path("delete_bookmark", delete_bookmark_view, name="delete-bookmark"),
    path("show_bookmarks", get_bookmarks_set, name="show-bookmarks"),
    path(
        "profile_settings", profile_settings_component, name="profile-settings"
    ),
    path("about_us", about_us, name="about-us"),
]

urlpatterns += htmx_paths
