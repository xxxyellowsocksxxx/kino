from django.urls import path, include

from movies.views import MoviesView, MovieDetailView, AddReview

urlpatterns = [
    path("", MoviesView.as_view(), name='movie_list'),
    path("<slug:slug>/detail/", MovieDetailView.as_view(), name='movie_detail'),
    path("review/<int:id>/", AddReview.as_view(), name='add_review'),
]
