from django.contrib import admin

from movies.models import *

admin.site.register(Category)
admin.site.register(FilmCrew)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShot)
admin.site.register(Rating)
admin.site.register(Review)
