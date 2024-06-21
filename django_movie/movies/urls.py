from django.urls import path

from movies.views import MoviesView, MovieDetailView, AddReview, FilmCrewView, FilterMoviesView

urlpatterns = [
    path("", MoviesView.as_view(), name='movie_list'),
    path("filter/", FilterMoviesView.as_view(), name='filter'),
    path("<slug:slug>/detail/", MovieDetailView.as_view(), name='movie_detail'),
    path("review/<int:id>/", AddReview.as_view(), name='add_review'),
    path("filmcrew/<str:slug>/detail/",
         FilmCrewView.as_view(), name='filmcrew_detail'),
]
