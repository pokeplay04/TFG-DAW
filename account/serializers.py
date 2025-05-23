# from rest_framework import serializers

# from .models import User, FriendshipRequest


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'friends_count', 'posts_count', 'get_avatar',)


# class FriendshipRequestSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
    
#     class Meta:
#         model = FriendshipRequest
#         fields = ('id', 'created_by',)


from rest_framework import serializers
from .models import SpotifyUser, FriendshipRequest

class SpotifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyUser
        fields = ['id', 'email', 'display_name', 'friends_count', 'posts_count', 'get_avatar']


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = SpotifyUserSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest  # ✅ Ahora sí está bien
        fields = ['id', 'created_by']
