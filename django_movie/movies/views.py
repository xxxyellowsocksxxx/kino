from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from movies.models import Movie, Category, FilmCrew, Genre
from movies.forms import ReviewForm


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(GenreYear, DetailView):
    """ Описание фильма """
    model = Movie
    slug_field = 'url'


class AddReview(View):
    """ Отзыв """

    def post(self, request, id):
        bound_form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=id)

        if bound_form.is_valid():
            bound_form = bound_form.save(commit=False)

            # присовение родителя отзыва
            if request.POST.get('parent', None):
                bound_form.parent_id = int(request.POST.get('parent'))

            bound_form.movie = movie
            bound_form.save()

        return redirect(movie.get_absolute_url())


class FilmCrewView(GenreYear, DetailView):
    """ Вывод информации о члене съёмочной группы """
    model = FilmCrew
    template_name = 'movies/filmcrew.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """ Фильтр фильмов """

    def get_queryset(self):
        query_set = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        # метод чтобы задоджить повторение по двум фильтрам
        return query_set.distinct()
