from __future__ import annotations

from typing import List

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import tmdbsimple as tmdb


class Film(models.Model):
    """
    Model for Film with film ID

    :param filmId: The ID of a specific film.
    :type filmId: int
    :param title: The title of a film.
    :type title: str
    :param year_released: The release year of the film.
    :type year_released: int
    :param director: The name of the director(s) of the film.
    :type director: str
    :param genres: The genres of the film.
    :type genres: str
    :param summary: A summary of the film.
    :type summary: str
    :param stars: The stars(actors and actresses) of the film
    :type stars: str
    """

    filmId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    year_released = models.IntegerField(null=True)
    director = models.CharField(max_length=512, blank=True)
    genres = models.CharField(max_length=512, blank=True)
    summary = models.CharField(max_length=1000, blank=True)
    stars = models.CharField(max_length=1000, blank=True)
    poster = models.CharField(max_length=265, blank=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.year_released})"

    def get_director(self) -> List[str]:
        """Get a list contain the name of the director(s) of the film

        :return: A list containing the string representing the name of the director(s) of the film
        """
        return [director.strip() for director in self.director.split(",")]

    def get_genres(self) -> List[str]:
        """Get a list contain the genres of the film

        :return: A list containing the string representing the genres of the film
        """
        return [genre.strip() for genre in self.genres.split(",")]

    def get_stars(self) -> List[str]:
        """Get a list contain the genres of the film

        :return: A list containing the string representing name of the stars of the film
        """
        return [star.strip() for star in self.stars.split(",")]

    def set_director(self, directors: List[str]):
        """Get a list containing the name of the director(s) of the film and set it to
        be a director attribute

        :param directors: A list containing the string representing the name of the director(s)
        of the film
        """
        self.director = ", ".join(directors)

    def set_genres(self, genres: List[str]):
        """Get a list containing the genres and set it to be a genres attribute

        :param genres: A list containing the string representing the genres of the film
        """
        self.genres = ", ".join(genres)

    def set_stars(self, stars: List[str]):
        """Get a list containing the stars of the film and set it to be a stars attribute

        :param stars: A list containing the string representing the stars of the film
        """
        self.stars = ", ".join(stars)

    @classmethod
    def get_film(cls, film_id: str) -> Film:
        """Create and return Film object

        :param film_id: The ID of a specific film.
        :type film_id: str
        :return: film object
        """
        num_id = int(film_id)

        try:
            film = cls.objects.get(pk=film_id)
        except cls.DoesNotExist:
            # tmdbsimple: get movie from movie id
            response_info = tmdb.Movies(num_id).info()
            response_credits = tmdb.Movies(num_id).credits()
            title = response_info["title"]

            summary = response_info["overview"]
            if summary == '':
                summary = "The summary of this film is unknown or not translated to English."

            year_released = response_info["release_date"].split("-")[0]
            if year_released == '':
                year_released = None

            # get film poster path
            path = response_info['poster_path']
            if path is None:
                poster = "https://i.ibb.co/2Kxk7XZ/no-poster.jpg"
            else:
                poster = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{path}"

            film = cls.objects.create(
                filmId=num_id,
                title=title,
                year_released=year_released,
                summary=summary,
                poster=poster
            )

            # get the list of the name of all directors
            directors = [
                director["name"]
                for director in response_credits["crew"]
                if director["job"] == "Director"
            ][:5]
            film.set_director(directors)

            # get the list of genres of the film
            genres_lst = [genres["name"] for genres in response_info["genres"]]
            film.set_genres(genres_lst)

            # get the list of the name of all stars
            stars = [star["name"] for star in response_credits["cast"]][:5]
            film.set_stars(stars)
            film.save()

        return film


class Review(models.Model):
    """
    Model for Review with Film object and publishing date

    :param film: A Film object
    :type film: Film
    :param pub_date: A date object representing the published date of the review
    :type pub_date: Datetime
    :param content: A string representation of the content of this Review
    :type content: str
    :param author: User who created the Review
    :type author: User
    """

    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        string = f"Review for {self.film} @ {self.pub_date}"
        if self.author:
            return string + f" by {self.author}"
        return string + " by anonymous"
