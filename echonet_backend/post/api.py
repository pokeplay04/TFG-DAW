from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import SpotifyUser, FriendshipRequest
from account.serializers import SpotifyUserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm, MusicAttachmentForm
from .models import Post, Like, Comment, Trend
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_list_profile(request, spotifyuser_pk):   
    user = SpotifyUser.objects.get(pk=spotifyuser_pk)
    posts = Post.objects.filter(created_by_id=spotifyuser_pk)

    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = SpotifyUserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    music_attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    music_attachment_form = MusicAttachmentForm(request.POST)

    if form.is_valid():
        # se crea el post
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        # se crea el attachment independientemente del post
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.created_by = request.user
            attachment.post = post
            attachment.save()

        # si se ha enviado un track_id, se crea el music attachment
        if request.data.get('track_id'):
            music_attachment_form = MusicAttachmentForm(request.POST)
            # se crea el music attachment independientemente del post
            if  music_attachment_form.is_valid():
                music_attachment = music_attachment_form.save(commit=False)
                music_attachment.created_by = request.user
                music_attachment.post = post
                music_attachment.save()

        
        # se suma al user un post
        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add somehting here later!...'})



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not Like.objects.filter(post=post, created_by=request.user).exists():
        # se crea el like
        like = Like.objects.create(post=post, created_by=request.user)
        # se suma el like al post
        post.likes_count = post.likes_count + 1
        # se guardan
        post.save()
        like.save()

        create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        # se elimina el like
        like = Like.objects.get(post=post, created_by=request.user)
        like.delete()
        # se resta el like al post
        post.likes_count = post.likes_count - 1
        # se guardan
        post.save()
        # create_notification(request, 'post_like', post_id=post.id)
        return JsonResponse({'message': 'like deleted'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_create_comment(request, pk):
    post = Post.objects.get(pk=pk)

    # se crea el comentario 
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user, post=post)

    # se suma el comentario al post
    post.comments_count = post.comments_count + 1
    post.save()

    create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    # se resta al user un post
    user = request.user
    user.posts_count = user.posts_count - 1
    user.save()
    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()


    return JsonResponse({'message': 'post reported'})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)