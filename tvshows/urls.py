from django.conf.urls import url
from . import views

app_name = 'tvshows'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tvshow_id>[0-9]+)/$', views.tvshow_detail, name='tvshow_detail'),
    url(r'^popular$', views.popular, name='popular'),
    url(r'^top_rated', views.top_rated, name='top_rated'),
    url(r'^on_the_air', views.on_the_air, name='on_the_air'),
    url(r'^airing_today', views.airing_today, name='airing_today'),
    url(r'^(?P<tvshow_id>[0-9]+)/cast&crew/$', views.cast, name='cast'),
    url(r'^(?P<tvshow_id>[0-9]+)/videos/$', views.videos, name='videos'),
    url(r'^(?P<tvshow_id>[0-9]+)/backdrops/$', views.backdrops, name='backdrops'),
    url(r'^(?P<tvshow_id>[0-9]+)/posters/$', views.posters, name='posters'),
]