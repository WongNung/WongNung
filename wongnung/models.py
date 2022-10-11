from django.db import models
from datetime import datetime
from decouple import config
# read API Key from .env file
API_KEY = config("API_KEY")


class Film(models.Model):
    filmId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    year_released = models.IntegerField()
    director = models.CharField(max_length=128, blank=True)
    genres = models.CharField(max_length=128, blank=True)
    summary = models.TextField()
    stars = models.CharField(max_length=196, blank=True)  # names of actors
    rating = models.FloatField(null=True, blank=True, default=None)

    def get_title(self):
        return self.title

    def get_year_released(self):
        return self.year_released

    def get_director(self):
        return [director.strip() for director in
                self.director.split(",")]

    def get_genres(self):
        return [genre.strip() for genre in
                self.genres.split(",")]

    def get_summary(self):
        return self.summary

    def get_stars(self):
        return [star.strip() for star in
                self.stars.split(",")]

    def get_rating(self):
        return str(self.rating)


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.now())
    content = models.TextField()
    # comment_set is auto-generated from Comment class, no need to include in the code.

    def get_content(self):
        return self.content
