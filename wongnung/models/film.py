from __future__ import annotations

from typing import List, Optional, Union

import tmdbsimple as tmdb
from django.db import models
from requests import HTTPError


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

    def get_director(self) -> Optional[List[str]]:
        """Get a list contain the name of the director(s) of the film

        :return: A list containing the string representing the names
                 of the director(s) of the film
        """
        return (
            [director.strip() for director in self.director.split(",")]
            if self.director
            else None
        )

    def get_genres(self) -> Optional[List[str]]:
        """Get a list contain the genres of the film

        :return: A list containing the string representing the genres of the film
        """
        return (
            [genre.strip() for genre in self.genres.split(",")]
            if self.genres
            else None
        )

    def get_stars(self) -> Optional[List[str]]:
        """Get a list contain the genres of the film

        :return: A list containing the string representing name of the stars of the film
        """
        return (
            [star.strip() for star in self.stars.split(",")]
            if self.stars
            else None
        )

    def set_director(self, directors: List[str]):
        """Get a list containing the name of the director(s) of the film and set it to
        be a director attribute

        :param directors: A list containing the string representing the names
                          of the director(s) of the film
        """
        self.director = ", ".join(directors)

    def set_genres(self, genres: List[str]):
        """Get a list containing the genres and set it to be a genres attribute

        :param genres: A list containing the string representing the genres of the film
        """
        self.genres = ", ".join(genres)

    def set_stars(self, stars: List[str]):
        """Get a list containing the stars of the film and set it to be
        a stars attribute

        :param stars: A list containing the string representing the stars of the film
        """
        self.stars = ", ".join(stars)

    @classmethod
    def get_film(cls, film_id: str) -> Union[Film, None]:
        """Create and return Film object

        :param film_id: The ID of a specific film.
        :return: film object
        """
        num_id = int(film_id)

        try:
            film = cls.objects.get(pk=film_id)
        except cls.DoesNotExist:
            try:
                film = cls.__create_film_with_details(num_id)
                cls.__update_film_credits(film)
            except HTTPError:
                return None

        return film

    @classmethod
    def __create_film_with_details(cls, film_id: int) -> "Film":
        """
        This creates a Film model with basic details.

        :param film_id: ID of film
        :return: Film instance
        :raises HTTPError: if film with the film_id returns non-OK response
        """
        film_details_response = tmdb.Movies(film_id).info()
        title = film_details_response["title"]
        summary = film_details_response["overview"]
        if not summary:
            summary = (
                "The summary of this film is unknown "
                + "or not translated to English."
            )
        try:
            year_released = film_details_response["release_date"].split("-")[0]
            if not year_released:
                year_released = None
        except KeyError:
            year_released = None

        path = film_details_response["poster_path"]
        if not path:
            poster = "https://i.ibb.co/2Kxk7XZ/no-poster.jpg"
        else:
            poster = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{path}"

        film = cls.objects.create(
            filmId=film_id,
            title=title,
            year_released=year_released,
            summary=summary,
            poster=poster,
        )

        genres_lst = [
            genres["name"] for genres in film_details_response["genres"]
        ]
        film.set_genres(genres_lst)
        film.save()

        return film

    @classmethod
    def __update_film_credits(cls, film: "Film"):
        """
        This updates a Film object with credits.

        :param film: Film instance
        :raises HTTPError: if film with has id that returns non-OK response
        """
        film_details_credits = tmdb.Movies(film.pk).credits()

        directors = [
            director["name"]
            for director in film_details_credits["crew"]
            if director["job"] == "Director"
        ][:5]
        film.set_director(directors)

        stars = [star["name"] for star in film_details_credits["cast"]][:5]
        film.set_stars(stars)
        film.save()
