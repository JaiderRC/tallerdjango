#primer entregable
# Activar venv
.\venv\Scripts\Activate.ps1

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Poblar datos
python poblar_datos.py
# 1. SerializerMethodField
¿Qué es?
SerializerMethodField es un campo de solo lectura en Django REST Framework que permite calcular y devolver valores personalizados basados en lógica de Python, en lugar de simplemente serializar campos del modelo.

Implementación en el proyecto:

class LibroSerializer(serializers.ModelSerializer):

    recent_reviews = serializers.SerializerMethodField()
    def get_recent_reviews(self, obj):
        reviews = obj.resenas.order_by('-fecha')[:5]
        return ResenaSerializer(reviews, many=True).data
Explicación:
get_recent_reviews es el método que define la lógica personalizada
obj representa la instancia del libro que se está serializando
La función retorna las 5 reseñas más recientes ordenadas por fecha descendente
Se usa ResenaSerializer para serializar las reseñas de forma anidada
Es de solo lectura y no se puede usar para crear o actualizar datos
Ventajas:
Flexibilidad para cálculos complejos
Puede acceder a relaciones y realizar agregaciones
Mantiene la estructura limpia del serializador principal

# 2. Filtros y Ordenamiento (django-filter)
Configuración:

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
}

# views.py
class LibroViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['autor', 'fecha_publicacion']
    ordering_fields = ['titulo', 'fecha_publicacion']
Tipos de Filtros Implementados:

# Filtrado por campos exactos:

URL: /api/libros/?autor=1

# Filtra libros del autor con ID 1

# Ordenamiento:

URL: /api/libros/?ordering=-fecha_publicacion

# Ordena libros por fecha de publicación descendente

URL: /api/libros/?ordering=titulo

Ordena alfabéticamente por título

# Filtrado personalizado:


def get_queryset(self):
    queryset = Libro.objects.all()
    if self.request.query_params.get('recent'):
        queryset = queryset.order_by('-created_at')[:10]
    return queryset
URL: /api/libros/?recent=true

 Retorna solo los 10 libros más recientes

# Ventajas:

Consultas eficientes a la base de datos

Interfaz de API flexible para clientes

Fácil de mantener y extender

# 3. Paginación
Configuración:


# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
# Comportamiento:
Divide grandes conjuntos de resultados en páginas
Cada página contiene máximo 10 elementos
Metadatos incluidos en la respuesta:
count: total de elementos
next: URL de la página siguiente
previous: URL de la página anterior
results: datos de la página actual
Ejemplo de respuesta:
json
{
    "count": 45,
    "next": "http://localhost:8000/api/libros/?page=2",
    "previous": null,
    "results": [
        // primeros 10 libros...
    ]
}
Beneficios:
Mejora el rendimiento con grandes volúmenes de datos
Mejor experiencia de usuario en frontend
Previene timeouts en peticiones grandes
# 4. Ruta Personalizada con @action
Implementación:
class LibroViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        libro = self.get_object()
        avg = libro.resenas.aggregate(Avg('calificacion'))['calificacion__avg']
        return Response({'average_rating': avg})
Parámetros del decorador @action:
detail=True: La acción opera sobre una instancia específica (requiere PK)
detail=False: La acción opera sobre la colección completa
methods: Lista de métodos HTTP permitidos (['get'], ['post'], etc.)
# Rutas generadas:

GET /api/libros/{pk}/average_rating/

Ejemplo: GET /api/libros/1/average_rating/

# Características:
Detail Action: Opera sobre un objeto específico identificado por PK
Collection Action: Opera sobre toda la colección (con detail=False)
Múltiples métodos: Puede aceptar GET, POST, PUT, etc.
Lógica personalizada: Puede contener cualquier lógica de negocio

# Casos de uso comunes:

# Cálculos y estadísticas
Acciones que no son CRUD estándar
Operaciones batch
Endpoints especializados para clientes específicos
# Ventajas:
Extiende la funcionalidad del ViewSet sin romper el patrón REST
Mantiene la coherencia en las URLs
Fácil de descubrir y usar
Integración automática con la documentación de la API

# Resumen de Integración
Estas características trabajan juntas para crear una API robusta:
SerializerMethodField → Personaliza la representación de datos
django-filter → Permite consultas específicas y eficientes
Paginación → Maneja grandes volúmenes de datos
@action → Extiende funcionalidad más allá del CRUD básico


