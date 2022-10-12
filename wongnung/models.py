from typing import List

from django.db import models
from datetime import datetime
import tmdbsimple as tmdb


class Film(models.Model):
    filmId = models.IntegerField(primary_key=True)  # Required
    title = models.CharField(max_length=256)  # Required
    year_released = models.IntegerField()  # Required
    director = models.CharField(max_length=512, blank=True)
    genres = models.CharField(max_length=512, blank=True)
    summary = models.CharField(max_length=1000, blank=True)
    stars = models.CharField(max_length=1000, blank=True)  # names of

    def get_director(self):
        return [director.strip() for director in
                self.director.split(",")]

    def get_genres(self):
        return [genre.strip() for genre in
                self.genres.split(",")]

    def get_stars(self):
        return [star.strip() for star in
                self.stars.split(",")]

    def set_director(self, directors: List[str]):
        self.director = ", ".join(directors)

    def set_genres(self, genres: List[str]):
        self.genres = ", ".join(genres)

    def set_stars(self, stars: List[str]):
        self.stars = ", ".join(stars)

    @classmethod
    def get_film(cls, film_id):
        try:
            film = cls.objects.get(pk=film_id)
            return film
        except cls.DoesNotExist:
            # tmdbsimple: get movie from movie id
            response_info = tmdb.Movies(film_id).info()
            response_credits = tmdb.Movies(film_id).credits()

            title = response_info['title']
            year_released = response_info['release_date'].split('-')[0]
            film = cls.objects.create(filmId=film_id, title=title, year_released=year_released)

            # get the list of the name of all directors
            directors = [director['name'] for director in response_credits['crew'] if director['job'] == 'Director']
            film.set_director(directors)

            # get the list of genres of the film
            genres_lst = [genres['name'] for genres in response_info['genres']]
            film.set_genres(genres_lst)

            # get the list of the name of all stars
            stars = [star['name'] for star in response_credits['cast']]
            film.set_stars(stars)

            return film


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.now())
    content = models.CharField(max_length=1000)
    # comment_set is auto-generated from Comment class, no need to include in the code.
