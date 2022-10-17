from .views import show_film_component, show_review_component
from django.urls import path

app_name = "wongnung"
urlpatterns = [
    path('show_film_component/<str:filmid>', show_film_component, name='film-component'),
    path('show_review_component/<int:pk>', show_review_component, name='review-component')
]
