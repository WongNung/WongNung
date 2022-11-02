from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .review import Review


class Report(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.user} reported {self.review} at {self.report_date}."
