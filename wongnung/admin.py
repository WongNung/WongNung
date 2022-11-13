from django.contrib import admin

from wongnung.models.fandom import Fandom
from wongnung.models.film import Film
from wongnung.models.report import Report
from wongnung.models.review import Review

# Register your models here.
admin.site.register(Film)
admin.site.register(Review)
admin.site.register(Fandom)
admin.site.register(Report)
