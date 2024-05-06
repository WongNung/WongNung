from abc import abstractmethod
from types import NoneType
from typing import Dict, List, Optional

from django.contrib.auth.models import User
from django.db.models import Q, query

from .models.review import Review
from .models.film import Film
from .models.fandom import Fandom


class UserActivity:
    """When a user does something on site,
    views can create an instance of activity."""

    film: Optional[Film]
    review: Optional[Review]
    fandom: Optional[Fandom]

    @abstractmethod
    def accepts(self) -> Q | NoneType:
        pass

    @abstractmethod
    def excludes(self):
        pass


class UserSeesFilm(UserActivity):
    """An activity when a user visits film details page"""

    def __init__(self, film: Film):
        self.film = film

    def accepts(self):
        return Q(film__title__iexact=self.film.title)

    def excludes(self):
        return None


class UserWritesReview(UserActivity):
    """An activity when a user writes a review for film"""

    def __init__(self, film: Film, review: Review):
        self.film = film
        self.review = review

    def accepts(self):
        query = Q(film__title__iexact=self.film.title)  # noqa
        for genre in self.film.get_genres():
            query |= Q(film__genres__icontains=genre)
        return query

    def excludes(self):
        return None


class UserUpvotesReview(UserActivity):
    """An activity when a user upvotes a review"""

    def __init__(self, film: Film, review: Review):
        self.film = film
        self.review = review

    def accepts(self):
        return Q(author__exact=self.review.author)

    def excludes(self):
        return None


class UserReportsReview(UserActivity):
    """An activity when a user reports a review"""

    def __init__(self, film: Film, review: Review):
        self.film = film
        self.review = review

    def accepts(self):
        return None

    def excludes(self):
        return Q(author__exact=self.review.author)


class UserJoinsFandom(UserActivity):
    """An activity when a user joins a fandom"""

    def __init__(self, fandom: Fandom):
        self.fandom = fandom

    def accepts(self):
        return Q(content__icontains=f"#{self.fandom.name}")

    def excludes(self):
        return None


class UserInsights:
    """A singleton for managing user activities"""

    users: Dict[User, List[UserActivity]] = dict()
    MAX_ACTIVITIES: int = 20

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(UserInsights, cls).__new__(cls)
        return cls.instance

    def _ensure_user(self, user: User) -> List[UserActivity]:
        """Ensure a user has their entry in the manager"""
        if user not in self.users.keys():
            self.users[user] = []
        return self.users[user]

    def get(self, user: User) -> List[UserActivity]:
        """Gets the list of activities for a user"""
        return self._ensure_user(user)

    def push(self, user: User, activity: UserActivity):
        """Push a new activity for a user"""
        user_insights = self.get(user)
        if len(user_insights) >= self.MAX_ACTIVITIES:
            user_insights.pop(0)
        user_insights.append(activity)
        self.users[user] = user_insights
        return user_insights
