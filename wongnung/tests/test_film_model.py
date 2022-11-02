"""Tests for Film model"""
from unittest.mock import patch
from django.test import TestCase
from ..tests.utils import (
    get_incomplete_response_info,
    get_missing_response_info,
    get_response_info,
    get_response_credits,
    MATRIX,
)
from ..models.film import Film


class FilmModelTests(TestCase):
    @patch("tmdbsimple.Movies.info", new=get_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def setUp(self):
        self.blank_film = Film()  # film object with blank attributes
        self.film = Film.get_film(MATRIX)

    def test_get_director(self):
        """
        get_director() returns a list of strings representing the director's
        name for a specific film.
        """

        self.assertListEqual(
            ["Lilly Wachowski", "Lana Wachowski"], self.film.get_director()
        )

    def test_get_genres(self):
        """
        get_director() returns a list of strings representing a specific film genres.
        """

        self.assertListEqual(
            ["Action", "Science Fiction"], self.film.get_genres()
        )

    def test_get_stars(self):
        """
        get_director() returns a list of strings representing the
        name of the star for a specific film.
        """

        self.assertListEqual(
            [
                "Keanu Reeves",
                "Laurence Fishburne",
                "Carrie-Anne Moss",
                "Hugo Weaving",
                "Joe Pantoliano",
            ],
            self.film.get_stars(),
        )

    def test_set_director(self):
        """
        set_director(directors) should set the director attribute as a comma-separated
        string representing the director's name for a specific film.
        """

        self.blank_film.set_director(["A", "B", "C"])
        self.assertEqual("A, B, C", self.blank_film.director)

    def test_set_genres(self):
        """
        set_genres(genres) should set the genres attribute as a comma-separated
        string representing the genres for a specific film.
        """
        self.blank_film.set_genres(["Action", "Comedy"])
        self.assertEqual("Action, Comedy", self.blank_film.genres)

    def test_set_stars(self):
        """
        set_stars(stars) should set the stars attribute as a comma-separated
        string representing the stars for a specific film.
        """

        self.blank_film.set_stars(["Robert", "Jimmy", "Jamie"])
        self.assertEqual("Robert, Jimmy, Jamie", self.blank_film.stars)

    def test_get_film(self):
        """
        get_film(film_id) should return the Film object.
        """

        matrix = self.blank_film.get_film(MATRIX)
        self.assertIsInstance(matrix, Film)

    @patch("tmdbsimple.Movies.info", new=get_incomplete_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_no_overview(self):
        """
        Film without overview should return placeholder message.
        """
        incomplete_film = Film.get_film("0")
        self.assertEqual(
            incomplete_film.summary,
            "The summary of this film is unknown or not translated to English.",
        )

    @patch("tmdbsimple.Movies.info", new=get_incomplete_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_no_poster(self):
        """
        Film without poster path should return placeholder poster link.
        """
        incomplete_film = Film.get_film("0")
        self.assertEqual(
            incomplete_film.poster, "https://i.ibb.co/2Kxk7XZ/no-poster.jpg"
        )

    @patch("tmdbsimple.Movies.info", new=get_incomplete_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_no_release_date(self):
        """
        Film without release date should return None.
        """
        incomplete_film = Film.get_film("0")
        self.assertIsNone(incomplete_film.year_released)

    @patch("tmdbsimple.Movies.info", new=get_missing_response_info)
    @patch("tmdbsimple.Movies.credits", new=get_response_credits)
    def test_explicit_no_release_date(self):
        """
        If there is no `release_date` key in response, return None.
        """
        incomplete_film = Film.get_film("0")
        self.assertIsNone(incomplete_film.year_released)
