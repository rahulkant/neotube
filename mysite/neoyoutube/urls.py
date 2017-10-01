from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_query/',views.search_query_view,name='search_query'),
    url(r'^watch/',views.watch_view,name='watch'),
    url(r'^channel/',views.channel_view,name='channel'),
]
