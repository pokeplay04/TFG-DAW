# urls de app Spotify
from django.urls import path
from . import api

urlpatterns = [
    path('search/', api.spotify_search, name='spotify_search'),
    path('now-playing/<str:spotifyuser_pk>/', api.get_now_playing, name='get_now_playing'),

]
