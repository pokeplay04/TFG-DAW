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
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return JsonResponse({'message': 'friendship request updated'})