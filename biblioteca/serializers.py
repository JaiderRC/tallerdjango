from rest_framework import serializers
from .models import Autor, Libro, Resena
class ResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resena
        fields = ['id', 'texto', 'calificacion', 'fecha']
class LibroSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='autor.nombre')
    recent_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'author_name', 'fecha_publicacion', 'resumen', 'recent_reviews']

    def get_recent_reviews(self, obj):
        reviews = obj.resenas.order_by('-fecha')[:5]
        return ResenaSerializer(reviews, many=True).data

    def validate_resumen(self, value):
        if value is None or len(str(value).strip()) < 30:
            raise serializers.ValidationError('El resumen debe tener al menos 30 caracteres.')
        return value
class AutorSerializer(serializers.ModelSerializer):
    libros = LibroSerializer(many=True, read_only=True)
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad', 'libros']

    def validate_nombre(self, value):
        if value is None or not str(value).strip():
            raise serializers.ValidationError('El nombre no puede estar vacío ni contener sólo espacios.')
        return value