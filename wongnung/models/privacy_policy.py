from django.db import models
from django.conf import settings

class PrivacyPolicy(models.Model):
    """
    A model that represents user's agreement to the privacy policy.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agreed = models.BooleanField(default=False)
