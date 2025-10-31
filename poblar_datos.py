import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')
django.setup()

from biblioteca.models import Autor, Libro, Resena
from django.utils import timezone

# Crear autores
autor1 = Autor.objects.create(nombre="Gabriel García Márquez", nacionalidad="Colombiano")
autor2 = Autor.objects.create(nombre="Isabel Allende", nacionalidad="Chilena")

# Crear libros
libro1 = Libro.objects.create(
    titulo="Cien años de soledad",
    autor=autor1,
    fecha_publicacion=timezone.datetime(1967, 6, 5),
    resumen="Una novela que narra la historia de la familia Buendía en el pueblo ficticio de Macondo."
)

libro2 = Libro.objects.create(
    titulo="La casa de los espíritus",
    autor=autor2,
    fecha_publicacion=timezone.datetime(1982, 1, 1),
    resumen="Una saga familiar que abarca varias generaciones en un país latinoamericano no identificado."
)

# Crear reseñas
Resena.objects.create(libro=libro1, texto="Una obra maestra de la literatura latinoamericana.", calificacion=5.0)
Resena.objects.create(libro=libro1, texto="Muy bueno, pero un poco confuso.", calificacion=4.0)
Resena.objects.create(libro=libro2, texto="Me encantó la historia y los personajes.", calificacion=4.5)