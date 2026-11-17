import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Post

TEMP_MEDIA = tempfile.mkdtemp()


def fake_image(name="test.png"):
    buffer = BytesIO()
    Image.new("RGB", (10, 10), "blue").save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class PostTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.author = User.objects.create_user("autora", password="ClaveSegura123")
        self.other = User.objects.create_user("otro", password="ClaveSegura123")
        self.post = Post.objects.create(
            title="Primer post", content="Contenido de prueba sobre Django", author=self.author
        )

    # --- Lectura (anónimo) ---
    def test_anonimo_ve_lista_y_detalle(self):
        self.assertContains(self.client.get(reverse("posts:list")), "Primer post")
        response = self.client.get(reverse("posts:detail", args=[self.post.pk]))
        self.assertContains(response, "Contenido de prueba")
        self.assertNotContains(response, "Editar")

    def test_detalle_sin_imagen_no_se_rompe(self):
        response = self.client.get(reverse("posts:detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(self.client.get(reverse("posts:list")), "Sin imagen")

    # --- Rutas protegidas ---
    def test_anonimo_es_redirigido_al_login(self):
        urls = [
            reverse("posts:create"),
            reverse("posts:update", args=[self.post.pk]),
            reverse("posts:delete", args=[self.post.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_anonimo_no_puede_crear_por_post(self):
        self.client.post(reverse("posts:create"), {"title": "X", "content": "Y"})
        self.assertEqual(Post.objects.count(), 1)

    def test_otro_usuario_no_puede_editar_ni_eliminar(self):
        self.client.login(username="otro", password="ClaveSegura123")
        self.assertEqual(self.client.get(reverse("posts:update", args=[self.post.pk])).status_code, 403)
        self.assertEqual(self.client.post(reverse("posts:delete", args=[self.post.pk])).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    # --- CRUD autenticado ---
    def test_crear_post_con_imagen(self):
        self.client.login(username="autora", password="ClaveSegura123")
        response = self.client.post(
            reverse("posts:create"),
            {"title": "Con imagen", "content": "Hola", "image": fake_image()},
        )
        nuevo = Post.objects.get(title="Con imagen")
        self.assertRedirects(response, nuevo.get_absolute_url())
        self.assertEqual(nuevo.author, self.author)
        self.assertTrue(nuevo.image.name.startswith("posts/"))
        self.assertContains(self.client.get(nuevo.get_absolute_url()), nuevo.image.url)

    def test_editar_post(self):
        self.client.login(username="autora", password="ClaveSegura123")
        self.client.post(
            reverse("posts:update", args=[self.post.pk]),
            {"title": "Título editado", "content": "Nuevo contenido"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Título editado")

    def test_eliminar_post(self):
        self.client.login(username="autora", password="ClaveSegura123")
        response = self.client.post(reverse("posts:delete", args=[self.post.pk]))
        self.assertRedirects(response, reverse("posts:list"))
        self.assertFalse(Post.objects.exists())

    # --- Búsqueda ---
    def test_busqueda_por_titulo_y_contenido(self):
        Post.objects.create(title="Recetas", content="Cocina casera", author=self.author)
        response = self.client.get(reverse("posts:list"), {"q": "primer"})
        self.assertContains(response, "Primer post")
        self.assertNotContains(response, "Recetas")
        response = self.client.get(reverse("posts:list"), {"q": "casera"})
        self.assertContains(response, "Recetas")

    def test_busqueda_sin_resultados(self):
        response = self.client.get(reverse("posts:list"), {"q": "zzzinexistente"})
        self.assertContains(response, "No se encontraron publicaciones")
