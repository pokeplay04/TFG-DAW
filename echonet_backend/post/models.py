import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince

from account.models import SpotifyUser


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('Post', related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(SpotifyUser, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(SpotifyUser, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    post = models.ForeignKey('Post', related_name='attachments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(SpotifyUser, related_name='post_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''
        
class PostMusicAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post =  models.ForeignKey('Post', related_name='post_music_attachments', on_delete=models.CASCADE)
    track_id = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='post_music_attachments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    is_private = models.BooleanField(default=False)

    likes_count = models.IntegerField(default=0)

    comments_count = models.IntegerField(default=0)

    reported_by_users = models.ManyToManyField(SpotifyUser, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
    

class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()