from django.db import models
from account.models import SpotifyUser
from post.models import Post
from chat.models import Conversation
import uuid
# Create your models here.

# User favorite tracks
class User_fav_tracks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track_id = models.CharField(max_length=255, blank=True, null=True)
    track_name = models.CharField(max_length=255, blank=True, null=True)
    track_artist = models.CharField(max_length=255, blank=True, null=True)
    track_image = models.URLField(blank=True, null=True)
    track_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='user_fav_tracks', on_delete=models.CASCADE)


# User favorite albums
class User_fav_albums(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album_id = models.CharField(max_length=255, blank=True, null=True)
    album_name = models.CharField(max_length=255, blank=True, null=True)
    album_artist = models.CharField(max_length=255, blank=True, null=True)
    album_image = models.URLField(blank=True, null=True)
    album_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='user_fav_albums', on_delete=models.CASCADE)

# User favorite artists
class User_fav_artists(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist_id = models.CharField(max_length=255, blank=True, null=True)
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    artist_image = models.URLField(blank=True, null=True)
    artist_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='user_fav_artists', on_delete=models.CASCADE)

# Post music attachment (embed)
class Post_music_attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post =  models.ForeignKey(Post, related_name='post_music_attachments', on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255, blank=True, null=True)
    embed_html = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='post_music_attachments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Chat music attachment (embed)
class Chat_music_attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='chat_music_attachments', on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255, blank=True, null=True)
    embed_html = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='chat_music_attachments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)