from django.test import TestCase
from django.db.utils import IntegrityError
from account.models import SpotifyUser
from .models import Conversation, ConversationMessage
import uuid

from django.db import IntegrityError, transaction, connection

from datetime import datetime, timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

class ConversationMessageTest(TestCase):
    def setUp(self):
        self.user1 = SpotifyUser.objects.create(
            id = 'id1',
            email= 'test@example.com',
            display_name='Test User',
            access_token='test_access_token',
            refresh_token='test_refresh_token',
            token_expires=datetime(2025, 5, 1, 0, 0, 0, tzinfo=timezone.utc),
            avatar=None,
            friends_count=0,
            posts_count=0,
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime(2023, 10, 1, 0, 0, 0, tzinfo=timezone.utc),
            last_login=datetime(2023, 10, 1, 0, 0, 0, tzinfo=timezone.utc),
            password='test_password',
        )
        self.user1.save()

        # Otro usuario si quieres
        self.user2 = SpotifyUser.objects.create(
            id = 'id2',
            email='test2@example.com',
            display_name='Test User 2',
            access_token='access_token_2',
            refresh_token='refresh_token_2',
            token_expires=datetime(2025, 5, 1, 0, 0, 0, tzinfo=timezone.utc),
            avatar=None,
            friends_count=1,
            posts_count=2,
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime(2023, 10, 2, 0, 0, 0, tzinfo=timezone.utc),
            last_login=datetime(2023, 10, 2, 0, 0, 0, tzinfo=timezone.utc),
            password='test_password',
        )
        self.user2.save()

        # Crear conversación con esos usuarios
        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user1, self.user2)
    
    def test_create_message_in_existing_conversation(self):
        """Crear mensaje en una conversación válida debe funcionar"""
        msg = ConversationMessage.objects.create(
            conversation=self.conversation,
            body="Hola, ¿cómo estás?",
            sent_to=self.user2,
            created_by=self.user1,
        )
        self.assertIsNotNone(msg.id)
        self.assertEqual(msg.body, "Hola, ¿cómo estás?")
        self.assertEqual(msg.conversation, self.conversation)
        self.assertEqual(msg.sent_to, self.user2)
        self.assertEqual(msg.created_by, self.user1)

    def test_user_not_in_conversation_cannot_send_message(self):
        """Un usuario que no pertenece a la conversación no debe poder enviar un mensaje"""
        # Crear un tercer usuario no involucrado en la conversación
        user3 = SpotifyUser.objects.create(
            id='id3',
            email='test3@example.com',
            display_name='User 3',
            access_token='access_token_3',
            refresh_token='refresh_token_3',
            token_expires=datetime(2025, 5, 1, 0, 0, 0, tzinfo=timezone.utc),
            avatar=None,
            friends_count=0,
            posts_count=0,
            is_active=True,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime(2023, 10, 3, 0, 0, 0, tzinfo=timezone.utc),
            last_login=datetime(2023, 10, 3, 0, 0, 0, tzinfo=timezone.utc),
            password='test_password',
        )
        user3.save()
        # Ejecuta el intento de crear mensaje — debe fallar porque user3 no está en la conversación
        with self.assertRaises(ValidationError) as context:
            ConversationMessage.objects.create(
                conversation=self.conversation,
                body="Este mensaje no debe permitirse",
                created_by=user3,
                sent_to=self.user1
            )

        self.assertIn("no pertenece a la conversación", str(context.exception))