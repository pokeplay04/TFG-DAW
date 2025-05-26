from rest_framework_simplejwt.tokens import RefreshToken
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

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def spotify_login(request):
    scope = 'user-read-email user-read-private'
    query = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.REDIRECT_URI,
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
        'redirect_uri': settings.REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }

    token_response = requests.post('https://accounts.spotify.com/api/token', data=payload)

    if token_response.status_code != 200:
        # Mostrar el error devuelto por Spotify
        error_message = token_response.text
        print("❌ Error al obtener token de Spotify:")
        print("Status code:", token_response.status_code)
        print("Response:", error_message)
        return JsonResponse({'error': 'No se pudo obtener token de Spotify', 'details': error_message}, status=token_response.status_code)

    try:
        token_data = token_response.json()
    except ValueError:
        return JsonResponse({'error': 'La respuesta de Spotify no es JSON válido'}, status=500)

    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    expires_in = token_data.get('expires_in')

    if not access_token:
        return JsonResponse({'error': 'Spotify no devolvió un token de acceso'}, status=400)

    user_profile_response = requests.get(
        'https://api.spotify.com/v1/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    if user_profile_response.status_code != 200:
        print("❌ Error al obtener perfil de usuario de Spotify")
        print("Status code:", user_profile_response.status_code)
        print("Response:", user_profile_response.text)

        try:
            error_json = user_profile_response.json()
        except ValueError:
            error_json = {'error': 'Respuesta no es JSON válido', 'raw': user_profile_response.text}

        return JsonResponse({
            'error': 'No se pudo obtener perfil de usuario de Spotify',
            'spotify_response': error_json,
        }, status=500)
    
    user_profile = user_profile_response.json()

    id = user_profile['id']
    email = user_profile['email']
    display_name = remove_non_ascii(user_profile['display_name'])

    token_expires = timezone.now() + datetime.timedelta(seconds=expires_in)

    avatar_url = user_profile['images'][0]['url'] if user_profile.get('images') else None
    avatar_file = None

    if avatar_url:
        response = requests.get(avatar_url)
        if response.status_code == 200:
            file_name = os.path.basename(urlparse(avatar_url).path) + '.jpg' or 'spotify_avatar.jpg'
            avatar_file = ContentFile(response.content, name=file_name)

    # Crear o actualizar el usuario
    user, created = SpotifyUser.objects.update_or_create(
        id=id,
        defaults={
            'email': email,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expires': token_expires
        }
    )

    # Si el usuario es nuevo, establecer avatar y nombre
    if created and avatar_file:
        user.avatar.save(avatar_file.name, avatar_file)
        user.save()
        
    if created and display_name:
        user.display_name = display_name
        user.save()

    login(request, user)

    # Generar JWT con SimpleJWT
    tokens = get_tokens_for_user(user)
    access_jwt = tokens['access']
    refresh_jwt = tokens['refresh']

    # Redirigir al frontend con los datos codificados en la URL
    params = {
        'access': access_jwt,
        'refresh': refresh_jwt,
        'id': user.id,
        'display_name': user.display_name,
        'email': user.email,
        'avatar': user.avatar.url if user.avatar else '',
    }

    redirect_url = f"{settings.FRONTEND_URL}?{urlencode(params)}"
    return HttpResponseRedirect(redirect_url)

def remove_non_ascii(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
