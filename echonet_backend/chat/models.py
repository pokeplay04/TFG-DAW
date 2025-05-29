import uuid

from django.db import models
from django.utils.timesince import timesince
from django.core.exceptions import ValidationError

from account.models import SpotifyUser


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(SpotifyUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    track_id = models.CharField(max_length=255, blank=True, null=True)

    
    def modified_at_formatted(self):
       return timesince(self.created_at)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(SpotifyUser, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(SpotifyUser, related_name='sent_messages', on_delete=models.CASCADE)
    
    def created_at_formatted(self):
       return timesince(self.created_at)

    def clean(self):
        if self.created_by not in self.conversation.users.all():
            raise ValidationError("El creador no pertenece a la conversación")
        if self.sent_to not in self.conversation.users.all():
            raise ValidationError("El receptor no pertenece a la conversación")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean() automáticamente
        super().save(*args, **kwargs)