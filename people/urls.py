from django.conf.urls import url
from . import views

app_name = 'people'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<people_id>[0-9]+)/$', views.people_detail, name='people_detail'),
]