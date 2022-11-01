"""Construct Utilities for testing"""

MATRIX = "603"


def get_response_info(_):
    return {
        "title": "The Matrix",
        "genres": [
            {"id": 28, "name": "Action"},
            {"id": 878, "name": "Science Fiction"},
        ],
        "overview": "Set in the 22nd century, The Matrix tells the "
        "story of a computer hacker who joins a group of "
        "underground insurgents fighting the vast and "
        "powerful computers who now rule the earth.",
        "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
        "release_date": "1999-03-30",
    }


def get_incomplete_response_info(_):
    return {
        "title": "The Matrix",
        "genres": [
            {"id": 28, "name": "Action"},
            {"id": 878, "name": "Science Fiction"},
        ],
        "overview": "",
        "poster_path": "",
        "release_date": "",
    }


def get_response_credits(_):
    return {
        "cast": [
            {"name": "Keanu Reeves", "character": "Thomas A. Anderson / Neo"},
            {"name": "Laurence Fishburne", "character": "Morpheus"},
            {"name": "Carrie-Anne Moss", "character": "Trinity"},
            {"name": "Hugo Weaving", "character": "Agent Smith"},
            {"name": "Joe Pantoliano", "character": "Cypher"},
        ],
        "crew": [
            {"name": "Lilly Wachowski", "job": "Director"},
            {"name": "Lana Wachowski", "job": "Director"},
        ],
    }
