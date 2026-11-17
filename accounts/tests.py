from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class AccountTests(TestCase):
    def test_registro_crea_usuario_perfil_e_inicia_sesion(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "nueva",
                "email": "nueva@example.com",
                "password1": "ClaveSegura123",
                "password2": "ClaveSegura123",
            },
        )
        self.assertRedirects(response, reverse("posts:list"))
        user = User.objects.get(username="nueva")
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertContains(self.client.get(reverse("posts:list")), "Cerrar sesión")

    def test_login_y_logout(self):
        User.objects.create_user("ana", password="ClaveSegura123")
        response = self.client.post(reverse("login"), {"username": "ana", "password": "ClaveSegura123"})
        self.assertRedirects(response, reverse("posts:list"))
        self.assertContains(self.client.get(reverse("posts:list")), "ana")

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("posts:list"))
        self.assertContains(self.client.get(reverse("posts:list")), "Iniciar sesión")

    def test_perfil_protegido_para_anonimo(self):
        for name in ("accounts:profile", "accounts:profile_edit"):
            url = reverse(name)
            self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")

    def test_editar_perfil(self):
        user = User.objects.create_user("ana", password="ClaveSegura123")
        self.client.login(username="ana", password="ClaveSegura123")
        self.client.post(
            reverse("accounts:profile_edit"),
            {"first_name": "Ana", "last_name": "López", "email": "ana@example.com", "bio": "Hola!"},
        )
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Ana")
        self.assertEqual(user.profile.bio, "Hola!")
