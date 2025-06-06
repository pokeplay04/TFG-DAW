# urls de app Spotify
from django.urls import path
from . import api

urlpatterns = [
    path('search/', api.spotify_search, name='spotify_search'),
    path('now-playing/', api.get_now_playing, name='get_now_playing'),
    path('top/', api.get_top_items, name='get_top_items'), #hay que pasarle id, type y time_range como query params
]
