import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class SpotifyUserManager(BaseUserManager):
    def create_user(self, id, email, display_name, **extra_fields):
        if not id:
            raise ValueError('El usuario debe tener un ID de Spotify')
        email = self.normalize_email(email)
        user = self.model(id=id, email=email, display_name=display_name, **extra_fields)
        user.set_unusable_password() #Sin contraseña porque se autentica con Spotify
        user.save(using=self._db)
        return user
    
    def create_superuser(self, id, email, display_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id, email, display_name, **extra_fields)


class SpotifyUser(AbstractBaseUser, PermissionsMixin):
    id  = models.CharField(primary_key=True, max_length=255, unique=True)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expires = models.DateTimeField()
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    banner = models.ImageField(upload_to='banners', blank=True, null=True)
    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)

    people_you_may_know = models.ManyToManyField('self')

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = SpotifyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id']


    def __str__(self):
        return self.display_name


    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return settings.WEBSITE_URL + '/media/avatars/default.jpg'



class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(SpotifyUser, related_name='received_friendshiprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='created_friendshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)



# User favorite tracks
class SpotifyUser_Fav_Tracks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track_id = models.CharField(max_length=255, blank=True, null=True)
    track_name = models.CharField(max_length=255, blank=True, null=True)
    track_artist = models.CharField(max_length=255, blank=True, null=True)
    track_image = models.URLField(blank=True, null=True)
    track_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='tracks', on_delete=models.CASCADE)


# User favorite albums
class SpotifyUser_Fav_Albums(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album_id = models.CharField(max_length=255, blank=True, null=True)
    album_name = models.CharField(max_length=255, blank=True, null=True)
    album_artist = models.CharField(max_length=255, blank=True, null=True)
    album_image = models.URLField(blank=True, null=True)
    album_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='albums', on_delete=models.CASCADE)

# User favorite artists
class SpotifyUser_Fav_Artists(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist_id = models.CharField(max_length=255, blank=True, null=True)
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    artist_image = models.URLField(blank=True, null=True)
    artist_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='artists', on_delete=models.CASCADE)
