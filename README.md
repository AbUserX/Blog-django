# 📝 Blog Web con Django

Blog web desarrollado con **Python y Django** como entrega final del curso. Permite que los usuarios se registren, inicien sesión y publiquen posts con imágenes, que cualquier visitante puede leer y buscar.

## Tecnologías

- Python 3.10 o superior
- Django 5.2
- SQLite (base de datos por defecto)
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)
- Bootstrap 5 (estilos, cargado por CDN)

## Funcionalidades principales

**Publicaciones**
- Listado de posts en la página de inicio, con paginación.
- Detalle de cada post.
- Crear, editar y eliminar posts desde la interfaz web (no solo desde el admin).
- Carga de imagen opcional por post; si un post no tiene imagen, se muestra un recuadro "Sin imagen" y el template no se rompe.
- Solo el autor de un post puede editarlo o eliminarlo.

**Usuarios**
- Registro, login y logout.
- Perfil con nombre, email, biografía e imagen de perfil (avatar), editable por el usuario.
- La interfaz cambia según el visitante sea anónimo o esté autenticado.

**Rutas protegidas**
- Crear, editar y eliminar posts, ver y editar el perfil requieren sesión iniciada.
- La protección se aplica en las views con `LoginRequiredMixin` y `@login_required`; un visitante anónimo es redirigido al login.

**Búsqueda**
- Buscador en la barra de navegación que filtra por título o contenido, y avisa cuando no hay coincidencias.

## Estructura del proyecto

```
blog-django/
├── config/          # Configuración del proyecto (settings, urls)
├── posts/           # App de publicaciones (modelo, vistas CRUD, búsqueda, tests)
├── accounts/        # App de usuarios (registro, perfil, tests)
├── templates/       # Templates HTML
├── static/css/      # Estilos propios
├── requirements.txt
├── .env.example
└── manage.py
```

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/blog-django.git
cd blog-django
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
```

- Windows: `venv\Scripts\activate`
- macOS / Linux: `source venv/bin/activate`

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Variables de entorno (opcional)

El proyecto funciona en desarrollo sin configurar nada. Si querés usar tu propia clave, copiá el archivo de ejemplo y completá los valores:

- Windows: `copy .env.example .env`
- macOS / Linux: `cp .env.example .env`

Las variables disponibles son `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS`.

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear un superusuario (para usar el panel de administración)

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador:

- Sitio: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

## Cómo probar el proyecto desde cero

El repositorio **no incluye** `db.sqlite3` ni la carpeta `media/`, para que el proyecto arranque con una base limpia. Después de los pasos de instalación:

1. Entrá a http://127.0.0.1:8000/ como visitante: vas a ver el listado vacío y los botones de iniciar sesión y registrarse.
2. Probá entrar a http://127.0.0.1:8000/post/nuevo/ sin sesión: te redirige al login.
3. Registrate en **Registrarse** (quedás con la sesión iniciada).
4. Creá un post con **+ Nuevo post**, con y sin imagen. La carpeta `media/` se crea sola al subir la primera imagen.
5. Desde el detalle del post, probá **Editar** y **Eliminar**.
6. Usá el buscador de la barra superior con una palabra del título o del contenido, y con una palabra que no exista.
7. Entrá a tu perfil (tu nombre de usuario en la barra) y editalo, cargando una imagen de perfil.
8. Cerrá sesión y verificá que vuelven a aparecer las opciones de visitante.

### Tests automáticos

El proyecto incluye tests de CRUD, imágenes, autenticación, rutas protegidas y búsqueda:

```bash
python manage.py test
```

## Autora

**Sofia** — Proyecto final del curso de Python y Django.

- GitHub: [@USUARIO](https://github.com/USUARIO)
