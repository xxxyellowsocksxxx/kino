from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод списка категорий"""

    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(quantity=5):
    """Список последних добавленных"""
    movies = Movie.objects.order_by('id')[:quantity]
    return {'last_movies': movies}
