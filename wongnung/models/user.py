from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.db import models
from pgcrypto import fields
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a superuser with the given email and password."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = fields.EmailPGPSymmetricKeyField(unique=True, max_length=255)
    first_name = fields.CharPGPSymmetricKeyField(max_length=30, blank=True)
    last_name = fields.CharPGPSymmetricKeyField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    username = fields.CharPGPSymmetricKeyField(max_length=150, unique=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username