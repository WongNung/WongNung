from django.core.cache.backends.db import DatabaseCache

class UnsafeKeyDatabaseCache(DatabaseCache):
    def validate_key(self, key: str) -> None:
        """Override key validation to supress unsafe key warnings"""
        pass

