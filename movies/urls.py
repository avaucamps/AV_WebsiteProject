from django.conf.urls import url
from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$', views.movies, name='index'),
    url(r'^(?P<movie_id>[0-9]+)/$', views.movie_detail, name='movie_detail'),
    url(r'^(?P<movie_id>[0-9]+)/castncrew/$', views.movie_cast, name='movie_cast'),
    url(r'^(?P<movie_id>[0-9]+)/videos/$', views.movie_videos, name='movie_videos'),
    url(r'^(?P<movie_id>[0-9]+)/backdrops/$', views.movie_backdrops, name='movie_backdrops'),
    url(r'^(?P<movie_id>[0-9]+)/posters/$', views.movie_posters, name='movie_posters'),
    url(r'^popular_movies$', views.popular_movies, name='popular_movies'),
    url(r'^top_rated_movies$', views.top_rated_movies, name='top_rated_movies'),
    url(r'^now_playing_movies$', views.now_playing_movies, name='now_playing_movies'),
    url(r'^upcoming_movies$', views.upcoming_movies, name='upcoming_movies'),
]
