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
            response = tmdb.Movies(film_id).info()
            title = response['title']
            year_released = response['release_date'].split('-')[0]
            film = cls.objects.create(filmId=film_id, title=title, year_released=year_released)
            # TODO: set director, genres, stars attribute in Film object ex. film.set_director()
            return film


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.now())
    content = models.CharField(max_length=1000)
    # comment_set is auto-generated from Comment class, no need to include in the code.
