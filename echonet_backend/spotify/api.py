from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import SpotifyTrackSerializer, SpotifyAlbumSerializer, SpotifyArtistSerializer
from account.models import SpotifyUser
from account.utils import get_valid_access_token
# Endpoint para buscar en Spotify
# Este se usará en:
#  - Buscar canción para añadir al post -> embed
#  - Buscar cancion para añadir a chat -> embed
#  - Buscar canción / artista / album para añadir a perfil -> "preview" componente
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def spotify_search(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type')
    if not query:
        return Response({'error': 'Falta el parámetro de búsqueda "q"'}, status=status.HTTP_400_BAD_REQUEST)

    # Este es el access token de Spotify guardado en la base de datos
    access_token = get_valid_access_token(request.user)

    # Hacemos la solicitud a la API de Spotify
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'q': query,
        'type': search_type,  # puedes ajustar según lo que busques
        'limit': 5
    }

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

    if response.status_code != 200: 
        return Response({
            'error': 'Error al buscar en Spotify',
            'spotify_response': response.json()
        }, status=response.status_code)

    data = response.json()

    # Adaptamos la respuesta para componente Vue
    items = []
    if search_type == 'album':
        for item in data.get('albums', {}).get('items', []):
            items.append({
                'id': item['id'],
                'title': item['name'],
                'artist': item['artists'][0]['name'],
                'image': item['images'][0]['url'] if item['images'] else '',
            })
        serializer = SpotifyAlbumSerializer(items, many=True)
    elif search_type == 'artist':
        for item in data.get('artists', {}).get('items', []):
            items.append({
                'id': item['id'],
                'title': item['name'],
                'image': item['images'][0]['url'] if item['images'] else '',
            })
        serializer = SpotifyArtistSerializer(items, many=True)

    elif search_type == 'track':
        for item in data.get('tracks', {}).get('items', []):
            items.append({
                'id': item['id'],
                'title': item['name'],
                'artist': item['artists'][0]['name'],
                'image': item['album']['images'][0]['url'] if item['album']['images'] else '',
            })
        serializer = SpotifyTrackSerializer(items, many=True)


    return Response({'results': serializer.data})


# Endpoint para obtener el embed de Spotify
#  - Para aañadir a post
#  - Para añadir a chat
@api_view(['GET'])
def get_spotify_embed(request):
    track_url = request.GET.get('url')
    if not track_url:
        return Response({'error': 'URL no proporcionada'}, status=400)

    oembed_url = 'https://open.spotify.com/oembed'
    response = requests.get(oembed_url, params={'url': track_url})
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'No se pudo obtener el embed'}, status=500)

# Endpoint para obtener la reproducción actual de un usuario de Spotify
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_now_playing(request):
    spotifyuser_pk = request.GET.get('spotifyuser_pk')
    try:
        target_user = SpotifyUser.objects.get(id=spotifyuser_pk)
        access_token = get_valid_access_token(target_user)
    except SpotifyUser.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data and 'item' in data:
            item = data['item']
            return Response({
                'id': item['id'],
                'title': item['name'],
                'artist': item['artists'][0]['name'],
                'image': item['album']['images'][0]['url'] if item['album']['images'] else '',
                'url': item['external_urls']['spotify'],
            })
        else:
            return Response({'message': 'No hay reproducción actual'}, status=204)
    else:
        return Response({'error': 'Error al obtener la reproducción actual'}, status=response.status_code)


# Endpoint para obtener los top items de un usuario especificando type y time_range
#  - Para seccion Descubrir musica
#  - Para compartir top items en perfil
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_top_items(request):
    spotifyuser_pk = request.GET.get('spotifyuser_pk')
    try:
        target_user = SpotifyUser.objects.get(id=spotifyuser_pk)
        access_token = get_valid_access_token(target_user)
    except SpotifyUser.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)

    search_type = request.GET.get('type')
    time_range = request.GET.get('time_range', 'medium_term')
    if not search_type:
        return Response({'error': 'Falta el parámetro "type"'}, status=400)
    if search_type not in ['artists', 'tracks']:
        return Response({'error': 'El parámetro "type" debe ser "artists" o "tracks"'}, status=400)
    if time_range not in ['short_term', 'medium_term', 'long_term']:
        return Response({'error': 'El parámetro "time_range" debe ser "short_term", "medium_term" o "long_term"'}, status=400)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'https://api.spotify.com/v1/me/top/{search_type}', headers=headers, params={'time_range': time_range, 'limit': 10})
    if response.status_code == 200:
        data = response.json()
        items = []
        if search_type == 'artists':
            for item in data.get('items', []):
                items.append({
                    'id': item['id'],
                    'name': item['name'],
                    'image': item['images'][0]['url'] if item['images'] else '',
                })
            serializer = SpotifyArtistSerializer(items, many=True)
        elif search_type == 'tracks':
            for item in data.get('items', []):
                items.append({
                    'id': item['id'],
                    'name': item['name'],
                    'artist': item['artists'][0]['name'],
                    'image': item['album']['images'][0]['url'] if item['album']['images'] else '',
                })
            serializer = SpotifyTrackSerializer(items, many=True)

        return Response({'results': serializer.data})
    else:
        return Response({'error': 'Error al obtener los top items'}, status=response.status_code)
    
