from django.shortcuts import redirect
from django.conf import settings
import requests
from .models import SpotifyUser
import urllib.parse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.utils import timezone
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import requests, os, datetime
import unicodedata
from urllib.parse import urlencode


CLIENT_ID = '78cc48f673894cf1b8a45ecc5ff98c16'
CLIENT_SECRET = '45acdd37e4bd4ae7809dd821717df2df'
REDIRECT_URI = 'http://127.0.0.1:8000/api/spotify/callback'
FRONTEND_URL = 'http://localhost:5173/signup'

def spotify_login(request):
    scope = 'user-read-email user-read-private'
    query = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope,
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query)
    return redirect(url)

def spotify_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'No se ha recibido código de Spotify'}, status=400)

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    token_response = requests.post('https://accounts.spotify.com/api/token', data=payload)
    token_data = token_response.json()

    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    expires_in = token_data.get('expires_in')

    if not access_token:
        return JsonResponse({'error': 'No access token returned by Spotify'}, status=400)

    user_profile = requests.get(
        'https://api.spotify.com/v1/me',
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    spotify_id = user_profile['id']
    email = user_profile['email']
    display_name = remove_non_ascii(user_profile['display_name'])
    
    token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)

    avatar_url = user_profile['images'][0]['url'] if user_profile.get('images') else None
    avatar_file = None

    if avatar_url:
        response = requests.get(avatar_url)
        if response.status_code == 200:
            file_name = os.path.basename(urlparse(avatar_url).path)+'.jpg' or 'spotify_avatar.jpg'
            avatar_file = ContentFile(response.content, name=file_name)

    # Crear o actualizar el usuario
    user, created = SpotifyUser.objects.update_or_create(
        spotify_id=spotify_id,
        defaults={
            'email': email,
            'display_name': display_name,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expires': token_expires
        }
    )

    if created and avatar_file:
        user.avatar.save(avatar_file.name, avatar_file)
        user.save()

    login(request, user)

    # Guardar también en la sesión si quieres
    request.session['spotify_token'] = access_token
    request.session['spotify_token_expiry'] = token_expires.isoformat() if token_expires else None

    # # ✅ Establecer cookies seguras
    # expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)

    # response = HttpResponseRedirect(FRONTEND_URL)  # Redirige al frontend
    # response.set_cookie('access', access_token, httponly=True, secure=True, samesite='Lax', expires=expires)
    # response.set_cookie('refresh', refresh_token, httponly=True, secure=True, samesite='Lax', expires=expires)
    # response.set_cookie('user_id', str(user.id), httponly=False, expires=expires)  # visible por JS si quieres
    # response.set_cookie('user_name', user.display_name, httponly=False, expires=expires)
    # response.set_cookie('user_email', user.email, httponly=False, expires=expires)
    # response.set_cookie('user_avatar', user.avatar.url if user.avatar else '', httponly=False, expires=expires)
    params = {
        'access': access_token,
        'refresh': refresh_token,
        'id': user.id,
        'display_name': user.display_name,
        'email': user.email,
        'avatar': user.avatar.url if user.avatar else '',
    }

    # Redirige al frontend con los datos en la URL
    url = f"{FRONTEND_URL}?{urlencode(params)}"
    return HttpResponseRedirect(url)

def remove_non_ascii(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
