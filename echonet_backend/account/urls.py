from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api
from . import views

urlpatterns = [
    path('me/', api.me, name='me'),
    # path('signup/', api.signup, name='signup'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback', views.spotify_callback, name='spotify_callback'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('editprofile/', api.editprofile, name='editprofile'),

    path('gallery/<str:pk>/', api.gallery, name='gallery'),  # pk is the SpotifyUser id
    path('gallery/<str:pk>/save/', api.save_favorite, name='save_favorite'),  # pk is the SpotifyUser id
    path('gallery/<str:pk>/delete/', api.delete_favorite, name='delete_favorite'),  # pk is the SpotifyUser id

    path('friends/suggested/', api.my_friendship_suggestions, name='my_friendship_suggestions'),
    path('friends/<str:pk>/', api.friends, name='friends'),
    path('friends/<str:pk>/request/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<str:pk>/<str:status>/', api.handle_request, name='handle_request'),
]