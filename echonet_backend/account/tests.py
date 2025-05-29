from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import SpotifyUser

User = get_user_model()

class SpotifyUserModelTest(TestCase):

    def setUp(self):
        self.test_email = 'test@example.com'
        self.user_data = {
            'email': self.test_email,
            'display_name': 'Test User',
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'token_expires': '2025-05-01T00:00:00Z',
            'avatar': None,
            'friends_count': 0,
            'posts_count': 0,
            'is_active': True,
            'is_superuser': False,
            'is_staff': False,
            'date_joined': '2023-10-01T00:00:00Z',
            'last_login': '2023-10-01T00:00:00Z',
            'password': 'test_password',
        }

    def test_create_user_successfully(self):
        """Debe poder crear un usuario SpotifyUser exitosamente"""
        user = SpotifyUser.objects.create(**self.user_data)
        self.assertEqual(SpotifyUser.objects.count(), 1)
        self.assertEqual(user.email, self.test_email)
        self.assertEqual(user.display_name, 'Test User')

    def test_create_user_with_existing_email_should_fail(self):
        """Crear un usuario con email duplicado debe fallar"""
        SpotifyUser.objects.create(**self.user_data)

        with self.assertRaises(IntegrityError):
            SpotifyUser.objects.create(**self.user_data)

    def test_create_user_with_invalid_email(self):
        """Intentar crear un usuario con un email inválido debe fallar si hay validación"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'email_invalido'

        user = SpotifyUser(**invalid_data)

        with self.assertRaises(ValidationError):
            user.full_clean()  # Esto dispara la validación de EmailField
            user.save()

    def test_create_user_missing_required_fields(self):
        """Faltar campos requeridos debería lanzar error"""
        incomplete_data = {
            'email': 'test2@example.com',
        }

        with self.assertRaises(Exception):
            SpotifyUser.objects.create(**incomplete_data)

    #crear tests para cambiar el display_name a "nuevo nombre" y verificar que se actualiza correctamente
    def test_update_display_name(self):
        """Debe poder actualizar el display_name de un usuario"""
        user = SpotifyUser.objects.create(**self.user_data)
        new_display_name = 'Nuevo Nombre'
        user.display_name = new_display_name
        user.save()

        updated_user = SpotifyUser.objects.get(id=user.id)
        self.assertEqual(updated_user.display_name, new_display_name)
