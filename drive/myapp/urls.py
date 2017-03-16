from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^genres/$', views.show_genres, name='show_genres'),
]