from rest_framework import serializers

from account.serializers import SpotifyUserSerializer

from .models import Post, PostAttachment, Comment, Trend, PostMusicAttachment


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)

class PostMusicAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMusicAttachment
        fields = ('id', 'get_track_id',)

class PostSerializer(serializers.ModelSerializer):
    created_by = SpotifyUserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    music_attachments = PostMusicAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'is_private', 'likes_count', 'comments_count', 'created_by', 'created_at_formatted', 'attachments', 'music_attachments') #


class CommentSerializer(serializers.ModelSerializer):
    created_by = SpotifyUserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'created_by', 'created_at_formatted',)


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = SpotifyUserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    music_attachments = PostMusicAttachmentSerializer(read_only=True, many=True)


    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count', 'created_by', 'created_at_formatted', 'comments', 'attachments', 'music_attachments')


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences',)