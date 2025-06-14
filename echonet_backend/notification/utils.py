from .models import Notification

from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None
    # Si la notificación es de tipo 'post_like' o 'post_comment', obtenemos el post y su creador
    if type_of_notification == 'post_like':
        body = f'¡{request.user.display_name} le ha dado like a uno de tus posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f'¡{request.user.display_name} ha comentado en uno de tus posts!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'¡{request.user.display_name} te ha enviado una solicitud de amistad!'
    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'¡{request.user.display_name} ha aceptado tu solicitud de amistad!'
    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'¡{request.user.display_name} ha rechazado tu solicitud de amistad!'

    # Si el creador de la notificación es el mismo que el usuario que la creó, no la guardamos
    if created_for == request.user:
        return None
    
    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        post_id=post_id,
        created_for=created_for
    )

    return notification