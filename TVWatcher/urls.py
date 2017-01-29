from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^movies/', include('movies.urls')),
    url(r'^people/', include('people.urls')),
    url(r'^tvshows/', include('tvshows.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^', include('movies.urls')),
]
