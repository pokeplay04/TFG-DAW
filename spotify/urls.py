# urls de app Spotify
from django.urls import path
from . import api

urlpatterns = [
    path('search/', api.spotify_search, name='spotify_search'),
]
