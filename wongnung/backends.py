import logging
from datetime import datetime, timedelta

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.cache import caches
from django.conf import settings

UserModel = get_user_model()
logger = logging.Logger("RateLimiter")
cache = caches["RATELIMIT"]

class RateLimitMixin(object):
    try:
        threshold = int(getattr(settings, 'RATE_LIMIT_THRESHOLD', 9))
        minutes = int(getattr(settings, 'RATE_LIMIT_MINUTES', 5))
    except TypeError as ex:
        logger.exception(ex)
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        
        # -- rate limit check --
        
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user