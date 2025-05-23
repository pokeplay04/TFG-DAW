from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import SpotifyTrackSerializer, SpotifyAlbumSerializer, SpotifyArtistSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def spotify_search(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search_type')
    if not query:
        return Response({'error': 'Falta el parámetro de búsqueda "q"'}, status=status.HTTP_400_BAD_REQUEST)

    # Este es el access token de Spotify guardado en la base de datos
    access_token = request.user.access_token

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
