from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from movies.models import Movie
from movies.forms import ReviewForm


class MoviesView(ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
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
