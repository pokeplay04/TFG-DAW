from django.urls import path

from . import api


urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<str:spotifyuser_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),  #Aqui usa la id del usuario
    path('<uuid:pk>/music/', api.add_music_to_chat, name='add_music_to_chat'),
]