from importlib.resources import path
from .views import show_film_component
from django.urls import path

app_name = "wongnung"
urlpatterns = [
    path('show_film_component/<str:filmid>', show_film_component, name='film-component')
]