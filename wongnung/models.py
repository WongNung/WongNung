from django.db import models


class Film(models.Model):
    filmId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    year_released = models.IntegerField()
    director = models.TextField()
    genres = models.TextField()
    summary = models.TextField()
    stars = models.TextField()  # names of actors
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


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    content = models.TextField()
    # comment_set is auto-generated from Comment class, no need to include in the code.

    def get_content(self):
        return self.content
