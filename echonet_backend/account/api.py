from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from notification.utils import create_notification

from .forms import ProfileForm
from .models import SpotifyUser, FriendshipRequest
from .serializers import SpotifyUserSerializer, FriendshipRequestSerializer
from spotify.serializers import SpotifyTrackSerializer, SpotifyAlbumSerializer, SpotifyArtistSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
    })


# metodo para obtener galería musical de un usuario (fav artists, albums, tracks)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def gallery(request, pk):
    user = SpotifyUser.objects.get(pk=pk)

    data = {
        'tracks': SpotifyTrackSerializer(user.tracks.all(), many=True).data,
        'albums': SpotifyAlbumSerializer(user.albums.all(), many=True).data,
        'artists': SpotifyArtistSerializer(user.artists.all(), many=True).data
    }

    return JsonResponse(data, safe=False)

# metodo para guardar un track_favorite, un album favorito o un artista favorito
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def save_favorite(request, pk):
    user = SpotifyUser.objects.get(pk=pk)
    item = request.data.get('item')
    item_type = request.data.get('type')


    if item_type == 'track':
        track_id = item.get('track_id')
        if track_id:
            user.tracks.create(
                track_id=item.get('track_id'),
                track_name=item.get('track_name'),
                track_artist=item.get('track_artist'),
                track_image=item.get('track_image'),
                track_url=item.get('track_url')
            )
            user.save()
            return JsonResponse({'message': 'Track added to favorites'})
        else:
            return JsonResponse({'message': 'No track_id provided'}, status=400)

    elif item_type == 'album':
        album_id = item.get('album_id')
        if album_id:
            user.albums.create(
                album_id=item.get('album_id'),
                album_name=item.get('album_name'),
                album_artist=item.get('album_artist'),
                album_image=item.get('album_image'),
                album_url=item.get('album_url')
            )
            user.save()
            return JsonResponse({'message': 'Album added to favorites'})
        else:
            return JsonResponse({'message': 'No album_id provided'}, status=400)

    elif item_type == 'artist':
        artist_id = item.get('artist_id')
        if artist_id:
            user.artists.create(
                artist_id=item.get('artist_id'),
                artist_name=item.get('artist_name'),
                artist_image=item.get('artist_image'),
                artist_url=item.get('artist_url')
            )
            user.save()
            return JsonResponse({'message': 'Artist added to favorites'})
        else:
            return JsonResponse({'message': 'No artist_id provided'}, status=400)

    else:
        return JsonResponse({'message': 'Invalid type'}, status=400)
    
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_favorite(request, pk):
    user = SpotifyUser.objects.get(pk=pk)
    item_id = request.data.get('item_id')
    item_type = request.data.get('type')

    if item_type == 'track':
        user.tracks.filter(id=item_id).delete()
        return JsonResponse({'message': 'Track removed from favorites'})

    elif item_type == 'album':
        user.albums.filter(id=item_id).delete()
        return JsonResponse({'message': 'Album removed from favorites'})

    elif item_type == 'artist':
        user.artists.filter(id=item_id).delete()
        return JsonResponse({'message': 'Artist removed from favorites'})

    else:
        return JsonResponse({'message': 'Invalid type'}, status=400)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def friends(request, pk):
    user = SpotifyUser.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse({
        'user': SpotifyUserSerializer(user).data,
        'friends': SpotifyUserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_friendship_suggestions(request):
    serializer = SpotifyUserSerializer(request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def editprofile(request):
    user = request.user
    print("User:", user)

    form = ProfileForm(request.POST, request.FILES, instance=user)
    print("Form data:", request.POST, request.FILES) 

    if form.is_valid():
        form.save()
    else:
        print("Form not valid:", form.errors)
        
    serializer = SpotifyUserSerializer(user)

    return JsonResponse({'message': 'information updated', 'user': serializer.data})
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def send_friendship_request(request, pk):
    user = SpotifyUser.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def handle_request(request, pk, status):
    user = SpotifyUser.objects.get(pk=pk)
    try:
        friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    except FriendshipRequest.DoesNotExist:
        return JsonResponse({'message': 'friendship request not found'}, status=404)

    if status == 'accepted':
        friendship_request.status = status
        friendship_request.save()

        user.friends.add(request.user)
        user.friends_count += 1
        user.save()

        request_user = request.user
        request_user.friends_count += 1
        request_user.save()

        create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

        return JsonResponse({'message': 'friendship request accepted'})
    elif status == 'rejected':
        friendship_request.delete()
        return JsonResponse({'message': 'friendship request rejected and deleted'})
    else:
        return JsonResponse({'message': 'invalid status'}, status=400)