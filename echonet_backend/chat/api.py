from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import SpotifyUser

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def conversation_get_or_create(request, spotifyuser_pk):
    user = SpotifyUser.objects.get(pk=spotifyuser_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe=False)

# metodo para almacenar la canción en la conversación
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_music_to_chat(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    if 'track_id' not in request.data:
        return JsonResponse({'error': 'track_id is required'}, status=400)

    conversation.track_id = request.data['track_id']
    conversation.save()

    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)