"""
Snippet for setting up django-types to correctly show ForeignKey type.
"""
from django.db.models import ForeignKey


def setup():
    for cls in [ForeignKey]:
        cls.__class_getitem__ = classmethod(  # type: ignore [attr-defined]
            lambda cls, *args, **kwargs: cls
        )
